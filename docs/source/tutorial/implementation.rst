=====================================
 Guidelines for Implementing Plugins
=====================================

Stevedore uses setuptools entry points to define and load plugins. An
entry point is standard way to refer to a named object defined inside
a Python module or package. The name can be a reference to any class,
function, or instance, as long as it is created when the containing
module is imported (i.e., it needs to be a module-level global).

Names and Namespaces
====================

Entry points are registered using a *name* in a *namespace*. 

Entry point names are usually considered user-visible. For example,
they frequently appear in configuration files where a driver is being
enabled.  Because they are public, names are typically as short as
possible while remaining descriptive. For example, database driver
plugin names might be "mysql", "postgresql", "sqlite", etc.

Namespaces, on the other hand, are an implementation detail, and while
they are known to developers they are not usually exposed to users.
The namespace naming syntax looks a lot like Python's package syntax
(``a.b.c``) but *namespaces do not correspond to Python packages*. It
can be convenient to use a package name as a namespace, but it's not
required at all.  The main feature of entry points is that they can be
discovered *across* packages. That means that a plugin can be
developed and installed completely separately from the application
that uses it, as long as they agree on the namespace and API.

Each namespace is owned by the code that consumes the plugins and is
used to search for entry points. The entry point names are typically
owned by the plugin, but they can also be defined by the consuming
code for named hooks (see :class:`~stevedore.hook.HookManager`).  The
names of entry points must be unique within a given distribution, but
are not necessarily unique in a namespace (again, for hook patterns).

Keeping it Simple
=================

After a lot of trial and error, the easiest way I have found to define
an API is to follow these steps:

1. Define a unique namespace for each API by combining the name of the
   application (or library) and a name of the API. Keep it
   shallow. For example, "cliff.formatters" or
   "ceilometer.pollsters.compute".
2. Use the `abc module`_ to create a base abstract class to define the
   behaviors required of plugins of the API. 
3. Create plugins by subclassing the base class and implementing the
   required methods.

Developers don't have to subclass from the base class, but it provides
a convenient way to document the API, and using an abstract base class
keeps you honest.

.. seealso::

   * `abc module`_
   * `Using setuptools entry points`_
   * `Package Discovery and Resource Access using pkg_resources`_
   * `Using Entry Points to Write Plugins | Pylons`_

.. _Using setuptools entry points: http://reinout.vanrees.org/weblog/2010/01/06/zest-releaser-entry-points.html
.. _Package Discovery and Resource Access using pkg_resources: http://pythonhosted.org/distribute/pkg_resources.html
.. _Using Entry Points to Write Plugins | Pylons: http://docs.pylonsproject.org/projects/pylons-webframework/en/latest/advanced_pylons/entry_points_and_plugins.html
.. _abc module: http://docs.python.org/2/library/abc.html
