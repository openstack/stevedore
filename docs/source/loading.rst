======================
 Patterns for Loading
======================

Setuptools entry points are registered as within a namespace that
defines the API expected by the plugin code. Each entry point has a
name, which does not have to be unique within a given namespace. The
flexibility of this name management system makes it possible to use
plugins in a variety of ways. The manager classes in stevedore wrap
:mod:`pkg_resources` to apply different rules matching the patterns
described here.

Drivers -- Single Name, Single Entry Point
==========================================

Specifying a *driver* for communicating with an external resource
(database, device, or remote application) is perhaps the most common
use of dynamically loaded libraries. Drivers support the abstracted
view of the resource so an application can work with different types
of resources. For example, drivers may connect to database engines,
load different file formats, or communicate with similar web services
from different providers.  Many drivers may be available for a given
application, but it is implied in the interface between the
application and the driver that only one driver will be used to manage
a given resource.

Examples of the *drivers* pattern include:

* database client libraries used by SQLAlchemy_
* cloud vendor API clients used by libcloud_

.. _SQLAlchemy: http://sqlalchemy.org/

.. _libcloud: http://libcloud.apache.org/

Hooks -- Single Name, Many Entry Points
=======================================

*Hooks*, *signals*, or *callbacks* are invoked based on an event
occuring within an application. All of the hooks for an application
may share a single namespace (e.g., ``my.application.hooks``) and use
a different name for the triggered event (e.g., ``startup`` and
``precommit``). Multiple entry points can share the same name within
the namespace, so that multiple hooks can be invoked when an event
occurs.

Examples of the *hooks* pattern include:

* Emacs `mode hook functions`_
* `Django signals`_

.. _Django signals: https://docs.djangoproject.com/en/dev/topics/signals/

.. _mode hook functions: http://www.gnu.org/software/emacs/manual/html_node/emacs/Hooks.html

Extensions -- Many Names, Many Entry Points
===========================================

The more general form of extending an application is to load
additional functionality by discovering add-on modules that use a
minimal API to inject themselves at runtime. Extensions typically want
to be notified that they have been loaded and are being used so they
can perform initialization or setup steps. An extension may replace
core functionality or add to it.

Examples of the *extensions* pattern include:

* `Django apps`_
* `Sphinx extensions`_
* `Trac Plugins`_

.. _Trac Plugins: http://trac.edgewall.org/wiki/TracPlugins

.. _Sphinx extensions: http://sphinx.pocoo.org/extensions.html

.. _Django apps: https://docs.djangoproject.com/en/dev/intro/tutorial01/
