"""ExtensionManager
"""

import pkg_resources

import logging


LOG = logging.getLogger(__name__)


class Extension(object):
    """Book-keeping object for tracking extensions.

    :param name: The entry point name.
    :type name: str
    :param entry_point: The EntryPoint instance returned by
        :mod:`pkg_resources`.
    :type entry_point: EntryPoint
    :param plugin: The value returned by entry_point.load()
    :param obj: The object returned by ``plugin(*args, **kwds)`` if the
                manager invoked the extension on load.
    """

    def __init__(self, name, entry_point, plugin, obj):
        self.name = name
        self.entry_point = entry_point
        self.plugin = plugin
        self.obj = obj


class ExtensionManager(object):
    """Base class for all of the other managers.

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

    def __init__(self, namespace,
                 invoke_on_load=False,
                 invoke_args=(),
                 invoke_kwds={}):
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
                LOG.exception(err)
        return

    def _load_one_plugin(self, ep, invoke_on_load, invoke_args, invoke_kwds):
        plugin = ep.load()
        if invoke_on_load:
            obj = plugin(*invoke_args, **invoke_kwds)
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

        The first argument to func(), 'ext', is the
        :class:`~stevedore.extension.Extension` instance.

        Exceptions raised from within func() are logged and ignored.

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
            self._invoke_one_plugin(response.append, func, e, args, kwds)
        return response

    def _invoke_one_plugin(self, response_callback, func, e, args, kwds):
        try:
            response_callback(func(e, *args, **kwds))
        except Exception as err:
            # FIXME: Provide an argument to control
            # whether to ignore exceptions in each
            # plugin or stop processing.
            LOG.error('error calling %r: %s', e.name, err)
            LOG.exception(err)

    def __iter__(self):
        return iter(self.extensions)
