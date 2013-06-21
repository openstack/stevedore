import logging

from .extension import ExtensionManager


LOG = logging.getLogger(__name__)


class EnabledExtensionManager(ExtensionManager):
    """Loads only plugins that pass a check function.

    The check_func argument should return a boolean, with ``True``
    indicating that the extension should be loaded and made available
    and ``False`` indicating that the extension should be ignored.

    :param namespace: The namespace for the entry points.
    :type namespace: str
    :param check_func: Function to determine which extensions to load.
    :type check_func: callable
    :param invoke_on_load: Boolean controlling whether to invoke the
        object returned by the entry point after the driver is loaded.
    :type invoke_on_load: bool
    :param invoke_args: Positional arguments to pass when invoking
        the object returned by the entry point. Only used if invoke_on_load
        is True.
    :type invoke_args: tuple
    :param invoke_kwds: Named arguments to pass when invoking
        the object returned by the entry point. Only used if invoke_on_load
        is True.
    :type invoke_kwds: dict
    :param propagate_map_exceptions: Boolean controlling whether exceptions
        are propagated up through the map call or whether they are logged and
        then ignored
    :type invoke_on_load: bool

    """

    def __init__(self, namespace, check_func, invoke_on_load=False,
                 invoke_args=(), invoke_kwds={},
                 propagate_map_exceptions=False):
        self.check_func = check_func
        super(EnabledExtensionManager, self).__init__(
            namespace,
            invoke_on_load=invoke_on_load,
            invoke_args=invoke_args,
            invoke_kwds=invoke_kwds,
            propagate_map_exceptions=propagate_map_exceptions,
        )

    def _load_one_plugin(self, ep, invoke_on_load, invoke_args, invoke_kwds):
        ext = super(EnabledExtensionManager, self)._load_one_plugin(
            ep, invoke_on_load, invoke_args, invoke_kwds,
        )
        if ext and not self.check_func(ext):
            LOG.debug('ignoring extension %r', ep.name)
            return None
        return ext
