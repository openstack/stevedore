==================
 Creating Plugins
==================

After a lot of trial and error, the easiest way I have found to define
an API is to follow these steps:

#. Use the `abc module`_ to create a base abstract class to define the
   behaviors required of plugins of the API.  Developers don't have to
   subclass from the base class, but it provides a convenient way to
   document the API, and using an abstract base class keeps you
   honest.
#. Create plugins by subclassing the base class and implementing the
   required methods.
#. Define a unique namespace for each API by combining the name of the
   application (or library) and a name of the API. Keep it
   shallow. For example, "cliff.formatters" or
   "ceilometer.pollsters.compute".

Example Plugin Set
==================

The example program in this tutorial will create a plugin set with
several data formatters, like what might be used by a command line
program to prepare data to be printed to the console.  Each formatter
will take as input a dictionary with string keys and built-in data
types as values. It will return as output an iterator that produces
the string with the data structure formatted based on the rules of the
specific formatter being used. The formatter's constructor lets the
caller specify the maximum width the output should have.

A Plugin Base Class
===================

Step 1 above is to define an abstract base class for the API that
needs to be implemented by each plugin. 

.. literalinclude:: ../../../stevedore/example/base.py
   :language: python
   :prepend: # stevedore/example/base.py

The constructor is a concrete method because subclasses do not need to
override it, but the :func:`format` method does not do anything useful
because there is no "default" implementation available.

Concrete Plugins
================

The next step is to create a couple of plugin classes with concrete
implementations of :func:`format`. A simple example formatter produces
output with each variable name and value on a single line.

.. literalinclude:: ../../../stevedore/example/simple.py
   :language: python
   :prepend: # stevedore/example/simple.py

An alternate implementation produces a reStructuredText `field list`_.

.. literalinclude:: ../../../stevedore/example/fields.py
   :language: python
   :prepend: # stevedore/example/fields.py

There are plenty of other formatting options, but these two examples
will give us enough to work with to demonstrate registering and using
pluins.

Registering the Plugins
=======================

To use setuptools entry points, you must package your application or
library using setuptools. The build and packaging process generates
metadata which is available after installation to find the plugins
provided by each python distribution. 

The entry points must be declared as belonging to a specific
namespace, so we need to pick one before going any further. These
plugins are formatters from the stevedore examples, so I will use the
namespace "stevedore.example.formatter". Now it is possible to provide
all of the necessary information in the packaging instructions:

.. literalinclude:: ../../../stevedore/example/setup.py
   :language: python
   :prepend: # stevedore/example/setup.py

The important lines are near the bottom where the ``entry_points``
argument to :func:`setup` is set. The value is a dictionary mapping
the namespace for the plugins to a list of their definitions. Each
item in the list should be a string with ``name = module:importable``
where *name* is the user-visible name for the plugin, *module* is the
Python import reference for the module, and *importable* is the name
of something that can be imported from inside the module.

.. literalinclude:: ../../../stevedore/example/setup.py
   :language: python
   :lines: 37-43

In this case, there are three plugins registered. The "simple" and
"field" plugins defined above, and a "plain" plugin, which is just an
alias for the simple plugin.

setuptools Metadata
===================

During the build, setuptools copies entry point definitions to a file
in the ".egg-info" directory for the package. For example, the file
for stevedore is located in ``stevedore.egg-info/entry_points.txt``:

::

    [stevedore.example.formatter]
    simple = stevedore.example.simple:Simple
    field = stevedore.example.fields:FieldList
    plain = stevedore.example.simple:Simple
    
    [stevedore.test.extension]
    t2 = stevedore.tests.test_extension:FauxExtension
    t1 = stevedore.tests.test_extension:FauxExtension

:mod:`pkg_resources` uses the ``entry_points.txt`` file from all of
the installed packages on the import path to find plugins. You should
not modify these files, except by changing the list of entry points in
``setup.py``.

.. _abc module: http://docs.python.org/2/library/abc.html
.. _field list: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists
