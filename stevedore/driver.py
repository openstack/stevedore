from .named import NamedExtensionManager


class DriverManager(NamedExtensionManager):
    """Load a single plugin with a given name from the namespace.

    :param namespace: The namespace for the entry points.
    :type namespace: str
    :param name: The name of the driver to load.
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
        super(DriverManager, self).__init__(
            namespace=namespace,
            names=[name],
            invoke_on_load=invoke_on_load,
            invoke_args=invoke_args,
            invoke_kwds=invoke_kwds,
        )
        if not self.extensions:
            raise RuntimeError('No %r driver found, looking for %r' %
                               (namespace, name))
        if len(self.extensions) > 1:
            raise RuntimeError('Multiple %r drivers found: %s' %
                               (namespace,
                                ','.join('%s:%s' % (e.entry_point.module_name,
                                                    e.entry_point.attrs[0])
                                         for e in self.extensions))
                               )

    def __call__(self, func, *args, **kwds):
        """Invokes func() for the single loaded extension.

        The signature for func() should be::

            def func(ext, *args, **kwds):
                pass

        The first argument to func(), 'ext', is the
        :class:`~stevedore.extension.Extension` instance.

        Exceptions raised from within func() are logged and ignored.

        :param func: Callable to invoke for each extension.
        :param args: Variable arguments to pass to func()
        :param kwds: Keyword arguments to pass to func()
        :returns: List of values returned from func()
        """
        results = self.map(func, *args, **kwds)
        if results:
            return results[0]

    @property
    def driver(self):
        """Returns the driver being used by this manager.
        """
        ext = self.extensions[0]
        return ext.obj if ext.obj else ext.plugin
