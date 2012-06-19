from .extension import ExtensionManager


class EnabledExtensionManager(ExtensionManager):
    """An ExtensionManager that only loads plugins that pass a check function.
    """

    def __init__(self, namespace, check_func, invoke_on_load=False,
                 invoke_args=(), invoke_kwds={}):
        self.check_func = check_func
        super(EnabledExtensionManager, self).__init__(namespace,
                                                      invoke_on_load=invoke_on_load,
                                                      invoke_args=invoke_args,
                                                      invoke_kwds=invoke_kwds,
                                                      )

    def _load_one_plugin(self, ep, invoke_on_load, invoke_args, invoke_kwds):
        if not self.check_func(ep):
            LOG.debug('ignoring extension %r', ep.name)
            return None
        return super(EnabledExtensionManager, self)._load_one_plugin(
            ep, invoke_on_load, invoke_args, invoke_kwds,
            )
