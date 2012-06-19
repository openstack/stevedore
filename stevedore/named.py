from .enabled import EnabledExtensionManager


class NamedExtensionManager(EnabledExtensionManager):
    """ExtensionManager that only loads the named extensions.

    This is useful for explictly enabling extensions in a
    configuration file, for example.
    """

    def __init__(self, namespace, names,
                 invoke_on_load=False, invoke_args=(), invoke_kwds={}):
        def check(ep):
            return ep.name in names
        super(NamedExtensionManager, self).__init__(namespace,
                                                    check,
                                                    invoke_on_load=invoke_on_load,
                                                    invoke_args=invoke_args,
                                                    invoke_kwds=invoke_kwds,
                                                    )
