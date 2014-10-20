=========
 History
=========

0.14

- Provide an option to control requirements checking when loading
  plugins, and disable it by default. This removes protection against
  loading the wrong version of a plugin, or that plugin's
  dependencies.

0.13

- Deprecate ``TestExtensionManager`` and replace with
  ``make_test_instance()`` class method to provide test classes that
  behave more like the production class, while still allowing the
  extensions to be injected for testing. (contributed by drocco-007)
- Include a work-around to avoid a cpython bug with atexit
  (#15881). (contributed by philiptzou)
- Update documentation to refer to setuptools instead of
  distribute. (contributed by westurner)
- Add pypy to the list of default test configurations.

0.12

- Fixes an exception when reporting on an error where multiple drivers
  have the same name (:issue:`25`, solution provided by clayg).
- Switch packaging to use pbr_.
- Add ``map_method()`` API to controllers.

.. _pbr: https://github.com/openstack-dev/pbr

0.11

- Fixes logging configuration under Python 2.6 with a NullHandler.
  (:issue:`2`)

0.10

- Adds ``propagate_map_exceptions`` parameter to all of the extension
  managers which specifies whether exceptions are propagated up 
  through the map call or logged and then ignored. The default is to
  preserve the current behavior of logging and ignoring exceptions.
  Christopher Yeoh <cyeoh@au1.ibm.com>

0.9

- Add ``name_order`` parameter to
  :class:`~stevedore.named.NamedExtensionManager` to coerce
  :func:`map` into processing the extensions in the order they are
  named when the manager is created, instead of the random order
  they may have been loaded. Contributed by Daniel Rocco.
- Change the
  :class:`~stevedore.dispatch.NamedDispatchExtensionManager` to ignore
  missing extensions (:issue:`14`).
- Add ``__getitem__`` to
  :class:`~stevedore.extension.ExtensionManager` for looking up
  individual plugins by name (:issue:`15`).
- Start working on the tutorial, :doc:`tutorial/index`.
- Remove dependency on distribute, now that it is merged back into
  setuptools 0.7 (:issue:`19`).

0.8

  - Ignore AssertionError exceptions generated when plugins are
    loaded.
  - Update :class:`~stevedore.named.NamedExtensionManager` to check
    the name of a plugin before loading its code to avoid importing
    anything we are not going to use.

0.7.2

  - Fix logging support for Python 2.6.

0.7.1

  - Fix an issue with logging configuration.

0.7

  - Add memoization to the entrypoint scanning code in
    :class:`~stevedore.extension.ExtensionManager` to avoid
    performance issues in situations where lots of managers are
    instantiated with the same namespace argument.

0.6

  - Change the :class:`~stevedore.enabled.EnabledExtensionManager` to
    load the extension before calling the check function so the plugin
    can be asked if it should be enabled.

0.5

  - Add :class:`~stevedore.tests.manager.TestExtensionManager` for
    writing tests for classes that use extension managers.

0.4

  - Removed the ``name`` argument to plugin constructors.
  - Added ``driver`` property to :class:`~stevedore.driver.DriverManager`.

0.3

  - Added dispatch managers for selecting among a set of plugins at
    runtime instead of load time.
  - Added ``__call__`` method to
    :class:`~stevedore.driver.DriverManager` so it can be invoked in a
    more natural fashion for a single plugin.

0.2

  - Added documentation

0.1

  - First public release
