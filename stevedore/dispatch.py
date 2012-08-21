from .enabled import EnabledExtensionManager


class DispatchExtensionManager(EnabledExtensionManager):
    """Loads all plugins and filters on execution.

    This is useful for long-running processes that need to pass
    different inputs to different extensions.

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
    """

    def map(self, filter_func, func, *args, **kwds):
        """Iterate over the extensions invoking func() for any where
        filter_func() returns True.

        The signature of filter_func() should be::

            def filter_func(ext, *args, **kwds):
                pass

        The first argument to filter_func(), 'ext', is the
        :class:`~stevedore.extension.Extension`
        instance. filter_func() should return True if the extension
        should be invoked for the input arguments.

        The signature for func() should be::

            def func(ext, *args, **kwds):
                pass

        The first argument to func(), 'ext', is the
        :class:`~stevedore.extension.Extension` instance.

        Exceptions raised from within filter_func() and func() are
        logged and ignored.

        :param filter_func: Callable to test each extension.
        :param func: Callable to invoke for each extension.
        :param args: Variable arguments to pass to func()
        :param kwds: Keyword arguments to pass to func()
        :returns: List of values returned from func()
        """
        if not self.extensions:
            # FIXME: Use a more specific exception class here.
            raise RuntimeError('No %s extensions found' % self.namespace)
        response = []
        for e in self.extensions:
            if filter_func(e, *args, **kwds):
                self._invoke_one_plugin(response.append, func, e, args, kwds)
        return response


class NameDispatchExtensionManager(DispatchExtensionManager):
    """Loads all plugins and filters on execution.

    This is useful for long-running processes that need to pass
    different inputs to different extensions and can predict the name
    of the extensions before calling them.

    :param namespace: The namespace for the entry points.
    :type namespace: str
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

    def __init__(self, namespace, check_func, invoke_on_load=False,
                 invoke_args=(), invoke_kwds={}):
        super(NameDispatchExtensionManager, self).__init__(
            namespace=namespace,
            check_func=check_func,
            invoke_on_load=invoke_on_load,
            invoke_args=invoke_args,
            invoke_kwds=invoke_kwds,
            )
        self.by_name = dict((e.name, e) for e in self.extensions)

    def map(self, names, func, *args, **kwds):
        """Iterate over the extensions invoking func() for any where
        the name is in the given list of names.

        The signature for func() should be::

            def func(ext, *args, **kwds):
                pass

        The first argument to func(), 'ext', is the
        :class:`~stevedore.extension.Extension` instance.

        Exceptions raised from within func() are logged and ignored.

        :param names: List or set of name(s) of extension(s) to invoke.
        :param func: Callable to invoke for each extension.
        :param args: Variable arguments to pass to func()
        :param kwds: Keyword arguments to pass to func()
        :returns: List of values returned from func()
        """
        response = []
        for name in names:
            e = self.by_name[name]
            self._invoke_one_plugin(response.append, func, e, args, kwds)
        return response
