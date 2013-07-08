================
 stevedore 0.10
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

- Adds ``propagate_map_exceptions`` parameter to all of the extension
  managers which specifies whether exceptions are propagated up 
  through the map call or logged and then ignored. The default is to
  preserve the current behavior of logging and ignoring exceptions.
  Christopher Yeoh <cyeoh@au1.ibm.com>

Installing
==========

Visit the stevedore_ project page for download links and installation
instructions.
