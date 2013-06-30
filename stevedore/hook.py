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
        self._name = name
        super(HookManager, self).__init__(
            namespace,
            [name],
            invoke_on_load=invoke_on_load,
            invoke_args=invoke_args,
            invoke_kwds=invoke_kwds,
        )

    @classmethod
    def make_test_instance(cls, available_extensions, name):
        """Construct a test HookManager

        Test instances are passed a list of extensions to work from rather
        than loading them from entry points, filtering the available
        extensions to only those extensions whose name matches the name
        argument.

        :param available_extensions: Pre-configured Extension instances
            available for use
        :type available_extensions: list of
            :class:`~stevedore.extension.Extension`
        :param name: The name of the hooks to use.
        :type name: str
        :return: The manager instance, initialized for testing

        """

        o = super(HookManager, cls).make_test_instance(available_extensions,
                                                       [name])
        o._name = name
        return o

    def __getitem__(self, name):
        """Return the named extensions.

        Accessing a HookManager as a dictionary (``em['name']``)
        produces a list of the :class:`Extension` instance(s) with the
        specified name, in the order they would be invoked by map().
        """
        if name != self._name:
            raise KeyError(name)
        return self.extensions
