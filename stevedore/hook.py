from .named import NamedExtensionManager


class HookManager(NamedExtensionManager):
    """Coordinate execution of extensions using a shared name.
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
