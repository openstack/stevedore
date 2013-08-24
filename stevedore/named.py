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
    :type propagate_map_exceptions: bool

    """

    def __init__(self, namespace, names,
                 invoke_on_load=False, invoke_args=(), invoke_kwds={},
                 name_order=False, propagate_map_exceptions=False):
        self._names = names
        self._name_order = name_order
        super(NamedExtensionManager, self).__init__(
            namespace,
            invoke_on_load=invoke_on_load,
            invoke_args=invoke_args,
            invoke_kwds=invoke_kwds,
            propagate_map_exceptions=propagate_map_exceptions,
        )

    @classmethod
    def make_test_instance(cls, available_extensions, names=None,
                           name_order=False, propagate_map_exceptions=False):
        """Construct a test NamedExtensionManager

        Test instances are passed a list of extensions to work from rather
        than loading them from entry points, filtering the available
        extensions to only those extensions whose names are listed in the
        names argument.

        :param available_extensions: Pre-configured Extension instances
            available for use
        :type available_extensions: list of
            :class:`~stevedore.extension.Extension`
        :param names: The names of the extensions to use.
        :type names: list(str)
        :param name_order: If true, sort the extensions to match the order
            used in ``names``.
        :type name_order: bool
        :param propagate_map_exceptions: Boolean controlling whether exceptions
            are propagated up through the map call or whether they are logged
            and then ignored
        :type propagate_map_exceptions: bool
        :return: The manager instance, initialized for testing

        """

        o = cls.__new__(cls)
        o.namespace = 'TESTING'
        o._names = names
        o._name_order = name_order

        # simulate excluding plugins not listed in names, which normally
        # happens in _load_one_plugin
        extensions = [extension for extension in available_extensions
                      if extension.name in names]

        o._init_plugins(extensions,
                        propagate_map_exceptions=propagate_map_exceptions)
        return o

    def _init_plugins(self, extensions, propagate_map_exceptions=False):
        super(NamedExtensionManager, self)._init_plugins(
            extensions, propagate_map_exceptions=propagate_map_exceptions)

        if self._name_order:
            self.extensions = [self[n] for n in self._names]

    def _load_one_plugin(self, ep, invoke_on_load, invoke_args, invoke_kwds):
        # Check the name before going any further to prevent
        # undesirable code from being loaded at all if we are not
        # going to use it.
        if ep.name not in self._names:
            return None
        return super(NamedExtensionManager, self)._load_one_plugin(
            ep, invoke_on_load, invoke_args, invoke_kwds,
        )
