===========================================================
stevedore -- Manage dynamic plugins for Python applications
===========================================================

.. image:: https://pypip.in/version/stevedore/badge.svg
    :target: https://pypi.python.org/pypi/stevedore/
    :alt: Latest Version

.. image:: https://pypip.in/download/stevedore/badge.svg?period=month
    :target: https://pypi.python.org/pypi/stevedore/
    :alt: Downloads

Python makes loading code dynamically easy, allowing you to configure
and extend your application by discovering and loading extensions
("*plugins*") at runtime. Many applications implement their own
library for doing this, using ``__import__`` or ``importlib``.
stevedore avoids creating yet another extension
mechanism by building on top of `setuptools entry points`_. The code
for managing entry points tends to be repetitive, though, so stevedore
provides manager classes for implementing common patterns for using
dynamically loaded extensions.

.. _setuptools entry points: http://packages.python.org/setuptools/pkg_resources.html#convenience-api

* Free software: Apache license
* Documentation: http://docs.openstack.org/developer/stevedore
* Source: http://git.openstack.org/cgit/openstack/stevedore
* Bugs: https://bugs.launchpad.net/python-stevedore

