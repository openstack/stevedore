=============================================================
 stevedore -- Manage Dynamic Plugins for Python Applications
=============================================================

Python makes loading code dynamically easy, allowing you to configure
and extend your application by discovering and loading extensions
("*plugins*") at runtime. Many applications implement their own
library for doing this, using ``__import__`` or
:mod:`importlib`. stevedore avoids creating yet another extension
mechanism by building on top of `setuptools entry points`_. The code
for managing entry points tends to be repetitive, though, so stevedore
provides manager classes for implementing common patterns for using
dynamically loaded extensions.

Contents:

.. toctree::
   :glob:
   :maxdepth: 2

   patterns_loading
   patterns_enabling
   tutorial/index
   managers
   sphinxext
   install
   essays/*

.. toctree::
   :maxdepth: 1

   history

.. _setuptools entry points: http://packages.python.org/setuptools/pkg_resources.html#convenience-api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
