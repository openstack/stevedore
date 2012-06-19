from .hook import HookManager


class DriverManager(HookManager):
    """Load a single plugin with a given name from the namespace.
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
        if not self.extensions:
            raise RuntimeError('No %r driver found' % namespace)
        if len(self.extensions) > 1:
            raise RuntimeError('Multiple %r drivers found: %s' %
                               (namespace,
                                ','.join('%s:%s' % (e.module_name, e.attrs[0])
                                         for e in self.extensions))
                               )
