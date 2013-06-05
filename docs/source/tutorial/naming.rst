===============================
 Guidelines for Naming Plugins
===============================

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
(``a.b.c``) but *namespaces do not correspond to Python
packages*. Using a Python package name for an entry point namespace is
an easy way to ensure a unique name, but it's not required at all.
The main feature of entry points is that they can be discovered
*across* packages. That means that a plugin can be developed and
installed completely separately from the application that uses it, as
long as they agree on the namespace and API.

Each namespace is owned by the code that consumes the plugins and is
used to search for entry points. The entry point names are typically
owned by the plugin, but they can also be defined by the consuming
code for named hooks (see :class:`~stevedore.hook.HookManager`).  The
names of entry points must be unique within a given distribution, but
are not necessarily unique in a namespace.
