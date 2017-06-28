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

.. toctree::
   :glob:
   :maxdepth: 2

   user/index
   reference/index
   install/index


.. _setuptools entry points: http://setuptools.readthedocs.io/en/latest/pkg_resources.html?#entry-points

.. rubric:: Indices and tables

* :ref:`genindex`
* :ref:`search`
