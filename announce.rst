================
 stevedore 0.13
================

.. tags:: stevedore release python

What is stevedore?
==================

Python makes loading code dynamically easy, allowing you to configure
and extend your application by discovering and loading extensions
("*plugins*") at runtime. Many applications implement their own
library for doing this, using ``__import__`` or
``importlib``. stevedore_ avoids creating yet another extension
mechanism by building on top of `setuptools entry points`_. The code
for managing entry points tends to be repetitive, though, so stevedore
provides manager classes for implementing common patterns for using
dynamically loaded extensions.

.. _stevedore: http://stevedore.readthedocs.org

.. _setuptools entry points: http://packages.python.org/distribute/pkg_resources.html#convenience-api


What's New?
===========

- Deprecate ``TestExtensionManager`` and replace with
  ``make_test_instance()`` class method to provide test classes that
  behave more like the production class, while still allowing the
  extensions to be injected for testing. (contributed by drocco-007)
- Include a work-around to avoid a cpython bug with atexit
  (#15881). (contributed by philiptzou)
- Update documentation to refer to setuptools instead of
  distribute. (contributed by westurner)
- Add pypy to the list of default test configurations.


Installing
==========

Visit the stevedore_ project page for download links and installation
instructions.
