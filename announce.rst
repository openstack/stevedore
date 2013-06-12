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

- Add ``name_order`` parameter to ``NamedExtensionManager`` to coerce
  ``map()`` into processing the extensions in the order they are named
  when the manager is created, instead of the random order they may
  have been loaded. Contributed by Daniel Rocco.
- Change the ``NamedDispatchExtensionManager`` to ignore missing
  extensions (issue 14).
- Add ``__getitem__`` to ``ExtensionManager`` for looking up
  individual plugins by name (issue 15).
- Start working on the tutorial
- Remove dependency on distribute, now that it is merged back into
  setuptools 0.7 (issue 19).

Installing
==========

Visit the stevedore_ project page for download links and installation
instructions.
