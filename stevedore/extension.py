"""ExtensionManager
"""

import pkg_resources

import logging


LOG = logging.getLogger(__name__)


class Extension(object):

    def __init__(self, name, entry_point, plugin, obj):
        self.name = name
        self.entry_point = entry_point
        self.plugin = plugin
        self.obj = obj


class ExtensionManager(object):

    def __init__(self, namespace, invoke_on_load=False, invoke_args=(), invoke_kwds={}):
        self.namespace = namespace
        self.extensions = []
        for ep in pkg_resources.iter_entry_points(self.namespace):
            LOG.debug('found extension %r', ep.name)
            try:
                ext = self._load_one_plugin(ep,
                                            invoke_on_load,
                                            invoke_args,
                                            invoke_kwds,
                                            )
                if ext:
                    self.extensions.append(ext)
            except KeyboardInterrupt:
                raise
            except Exception as err:
                LOG.error('Could not load %r: %s', ep.name, err)
        return

    def _load_one_plugin(self, ep, invoke_on_load, invoke_args, invoke_kwds):
        plugin = ep.load()
        if invoke_on_load:
            obj = plugin(ep.name, *invoke_args, **invoke_kwds)
        else:
            obj = None
        return Extension(ep.name, ep, plugin, obj)

    def names(self):
        "Returns the names of the discovered extensions"
        return [e.name for e in self.extensions]

    def map(self, func, *args, **kwds):
        """Iterate over the extensions invoking func() for each.

        The signature for func() should be::

            def func(ext, *args, **kwds):
                pass

        The first argument to func(), 'ext', is the Extension
        instance.

        Exceptions raised from within func() are logged and ignored.

        :param func: Callable to invoke for each extension.
        :param args: Variable arguments to pass to func()
        :param kwds: Keyword arguments to pass to func()
        :returns: List of values returned from func()
        """
        if not self.extensions:
            raise RuntimeError('No %s extensions found' % self.namespace)
        response = []
        for e in self.extensions:
            try:
                response.append(func(e, *args, **kwds))
            except Exception as err:
                LOG.error('error calling %r: %s', e.name, err)
        return response

    def __iter__(self):
        return iter(self.extensions)


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


class NamedExtensionManager(EnabledExtensionManager):
    """ExtensionManager that only loads the named extensions.

    This is useful for explictly enabling extensions in a
    configuration file, for example.
    """

    def __init__(self, namespace, names=[],
                 invoke_on_load=False, invoke_args=(), invoke_kwds={}):
        def check(ep):
            return ep.name in names
        super(NamedExtensionManager, self).__init__(namespace,
                                                    check,
                                                    invoke_on_load=invoke_on_load,
                                                    invoke_args=invoke_args,
                                                    invoke_kwds=invoke_kwds,
                                                    )
