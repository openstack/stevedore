=========
 History
=========

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
