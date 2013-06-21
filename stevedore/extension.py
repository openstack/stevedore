"""ExtensionManager
"""

import pkg_resources

import logging


LOG = logging.getLogger(__name__)


class Extension(object):
    """Book-keeping object for tracking extensions.

    The arguments passed to the constructor are saved as attributes of
    the instance using the same names, and can be accessed by the
    callables passed to :meth:`map` or when iterating over an
    :class:`ExtensionManager` directly.

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
    :param propagate_map_exceptions: Boolean controlling whether exceptions
        are propagated up through the map call or whether they are logged and
        then ignored
    :type invoke_on_load: bool

    """

    def __init__(self, namespace,
                 invoke_on_load=False,
                 invoke_args=(),
                 invoke_kwds={},
                 propagate_map_exceptions=False):
        self.namespace = namespace
        self.propagate_map_exceptions = propagate_map_exceptions
        self.extensions = self._load_plugins(invoke_on_load,
                                             invoke_args,
                                             invoke_kwds)
        self._extensions_by_name = None

    ENTRY_POINT_CACHE = {}

    def _find_entry_points(self, namespace):
        if namespace not in self.ENTRY_POINT_CACHE:
            eps = list(pkg_resources.iter_entry_points(namespace))
            self.ENTRY_POINT_CACHE[namespace] = eps
        return self.ENTRY_POINT_CACHE[namespace]

    def _load_plugins(self, invoke_on_load, invoke_args, invoke_kwds):
        extensions = []
        for ep in self._find_entry_points(self.namespace):
            LOG.debug('found extension %r', ep)
            try:
                ext = self._load_one_plugin(ep,
                                            invoke_on_load,
                                            invoke_args,
                                            invoke_kwds,
                                            )
                if ext:
                    extensions.append(ext)
            except (KeyboardInterrupt, AssertionError):
                raise
            except Exception as err:
                LOG.error('Could not load %r: %s', ep.name, err)
                LOG.exception(err)
        return extensions

    def _load_one_plugin(self, ep, invoke_on_load, invoke_args, invoke_kwds):
        plugin = ep.load()
        if invoke_on_load:
            obj = plugin(*invoke_args, **invoke_kwds)
        else:
            obj = None
        return Extension(ep.name, ep, plugin, obj)

    def names(self):
        "Returns the names of the discovered extensions"
        # We want to return the names of the extensions in the order
        # they would be used by map(), since some subclasses change
        # that order.
        return [e.name for e in self.extensions]

    def map(self, func, *args, **kwds):
        """Iterate over the extensions invoking func() for each.

        The signature for func() should be::

            def func(ext, *args, **kwds):
                pass

        The first argument to func(), 'ext', is the
        :class:`~stevedore.extension.Extension` instance.

        Exceptions raised from within func() are propagated up and
        processing stopped if self.propagate_map_exceptions is True,
        otherwise they are logged and ignored.

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
            if self.propagate_map_exceptions:
                raise
            else:
                LOG.error('error calling %r: %s', e.name, err)
                LOG.exception(err)

    def __iter__(self):
        """Produce iterator for the manager.

        Iterating over an ExtensionManager produces the :class:`Extension`
        instances in the order they would be invoked.
        """
        return iter(self.extensions)

    def __getitem__(self, name):
        """Return the named extension.

        Accessing an ExtensionManager as a dictionary (``em['name']``)
        produces the :class:`Extension` instance with the
        specified name.
        """
        if self._extensions_by_name is None:
            d = {}
            for e in self.extensions:
                d[e.name] = e
            self._extensions_by_name = d
        return self._extensions_by_name[name]
