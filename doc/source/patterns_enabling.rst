=======================
 Patterns for Enabling
=======================

The entry point registry maintained by setuptools lists the available
plugins, but does not provide a way for the end-user to control which
are used or enabled. The common patterns for managing the set of
extensions to be used are described below.

Enabled Through Installation
============================

For many applications, simply installing an extension is enough of an
indication that the extension should be used. No explicit
configuration is required on the part of the user to either discover
or enable the extension, since its entry point can be discovered when
all of the plugins are loaded at runtime.

Examples of enabling through installation include:

* `python-openstackclient`_
* virtualenvwrapper_

.. _python-openstackclient: https://github.com/openstack/python-openstackclient
.. _virtualenvwrapper: http://pypi.python.org/pypi/virtualenvwrapper

Enabled Explicitly
==================

In other cases, the extensions may be installed system-wide but should
not all be enabled for a given application or instance of an
application. In these situations, the person deploying or using the
application will want to select the extensions to be used through an
explicit configuration step.

Examples of explicitly enabled extensions include:

* `Django apps`_
* `Sphinx extensions`_
* `Trac Plugins`_

.. _Trac Plugins: http://trac.edgewall.org/wiki/TracPlugins

.. _Sphinx extensions: http://sphinx.pocoo.org/extensions.html

.. _Django apps: https://docs.djangoproject.com/en/dev/intro/tutorial01/

.. seealso::

   :class:`stevedore.named.NamedExtensionManager`


Self-Enabled
============

Finally, some applications ask their extensions whether they should be
enabled. The extension may look at other libraries installed on the
system, check an external configuration setting, or examine a resource
to see if it can be managed by the plugin. These checks are usually at
runtime, either when the extension is loaded or when the user tries to
access a specific resource.

Examples of self-enabled extensions include:

* anydbm_
* PIL_

.. _anydbm: http://docs.python.org/library/anydbm.html
.. _PIL: http://www.pythonware.com/products/pil/

.. seealso::

   :class:`stevedore.enabled.EnabledExtensionManager`
