from .named import NamedExtensionManager


class HookManager(NamedExtensionManager):
    """Coordinate execution of multiple extensions using a common name.

    :param namespace: The namespace for the entry points.
    :type namespace: str
    :param name: The name of the hooks to load.
    :type name: str
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
    """

    def __init__(self, namespace, name,
                 invoke_on_load=False, invoke_args=(), invoke_kwds={}):
        super(HookManager, self).__init__(
            namespace,
            [name],
            invoke_on_load=invoke_on_load,
            invoke_args=invoke_args,
            invoke_kwds=invoke_kwds,
            )
