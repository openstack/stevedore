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
            LOG.debug('found extension %r', ep)
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
                LOG.exception(err)
        return response

    def __iter__(self):
        return iter(self.extensions)
