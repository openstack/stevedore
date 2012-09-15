=========
 History
=========

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
