from .extension import ExtensionManager


class NamedExtensionManager(ExtensionManager):
    """Loads only the named extensions.

    This is useful for explicitly enabling extensions in a
    configuration file, for example.

    :param namespace: The namespace for the entry points.
    :type namespace: str
    :param names: The names of the extensions to load.
    :type names: list(str)
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
    :param name_order: If true, sort the loaded extensions to match the
        order used in ``names``.
    :type name_order: bool
    :param propagate_map_exceptions: Boolean controlling whether exceptions
        are propagated up through the map call or whether they are logged and
        then ignored
    :type invoke_on_load: bool
    """

    def __init__(self, namespace, names,
                 invoke_on_load=False, invoke_args=(), invoke_kwds={},
                 name_order=False, propagate_map_exceptions=False):
        self._names = names
        super(NamedExtensionManager, self).__init__(
            namespace,
            invoke_on_load=invoke_on_load,
            invoke_args=invoke_args,
            invoke_kwds=invoke_kwds,
            propagate_map_exceptions=propagate_map_exceptions,
        )

        if name_order:
            ext_map = dict((x.name, x) for x in self.extensions)
            self.extensions = [ext_map[n] for n in names]

    def _load_one_plugin(self, ep, invoke_on_load, invoke_args, invoke_kwds):
        # Check the name before going any further to prevent
        # undesirable code from being loaded at all if we are not
        # going to use it.
        if ep.name not in self._names:
            return None
        return super(NamedExtensionManager, self)._load_one_plugin(
            ep, invoke_on_load, invoke_args, invoke_kwds,
        )
