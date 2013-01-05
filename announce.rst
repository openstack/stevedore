===============
 stevedore 0.8
===============

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

- Ignore AssertionError exceptions generated when plugins are
  loaded.
- Update ``NamedExtensionManager`` to check the name of a plugin
  before loading its code to avoid importing anything we are not going
  to use.

Installing
==========

Visit the stevedore_ project page for download links and installation
instructions.
