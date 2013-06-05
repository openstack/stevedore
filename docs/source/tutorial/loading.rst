=====================
 Loading the Plugins
=====================

There are several different enabling and invocation patterns for
consumers of plugins, depending on your needs.

Loading Drivers
===============

The most common way plugins are used is as individual drivers. In this
case, there may be many plugin options to choose from, but only one
needs to be loaded and called. The
:class:`~stevedore.driver.DriverManager` class supports this pattern.

This example program uses a :class:`DriverManager` to load a formatter
defined in the examples for stevedore. It then uses the formatter to
convert a data structure to a text format, which it can print.

.. literalinclude:: ../../../stevedore/example/load_as_driver.py
   :language: python
   :prepend: # stevedore/example/load_as_driver.py

The manager takes the plugin namespace and name as arguments, and uses
them to find the plugin. Then, because ``invoke_on_load`` is true, it
calls the object loaded. In this case that object is the plugin class
registered as a formatter. The ``invoke_args`` are positional
arguments passed to the class constructor, and are used to set the
maximum width parameter.

.. literalinclude:: ../../../stevedore/example/load_as_driver.py
   :language: python
   :lines: 30-35

After the manager is created, it holds a reference to a single object
returned by calling the code registered for the plugin. That object is
the actual driver, in this case an instance of the formatter class
from the plugin. The single driver can be accessed via the
:attr:`driver` property of the manager, and then its methods can be
called directly.

.. literalinclude:: ../../../stevedore/example/load_as_driver.py
   :language: python
   :lines: 36-37

Running the example program produces this output:

.. literalinclude:: driver_output.txt

Loading Extensions
==================

Another common use case is to load several extensions at one time, and
do something with all of them. Several of the other manager classes
support this invocation pattern, including
:class:`~stevedore.extension.ExtensionManager`,
:class:`~stevedore.named.NamedExtensionManager`, and
:class:`~stevedore.enabled.EnabledExtensionManager`.

.. literalinclude:: ../../../stevedore/example/load_as_extension.py
   :language: python
   :prepend: # stevedore/example/load_as_extension.py

The :class:`ExtensionManager` is created slightly differently from the
:class:`DriverManager` because it does not need to know in advance
which plugin to load. It loads all of the plugins it finds.

.. literalinclude:: ../../../stevedore/example/load_as_extension.py
   :language: python
   :lines: 24-28

To call the plugins, use the :meth:`map` method, passing a callable to
be invoked for each extension. The :func:`format_data` function used
with :meth:`map` in this example takes two arguments, the
:class:`~stevedore.extension.Extension` and the data argument given to
:meth:`map`.

.. literalinclude:: ../../../stevedore/example/load_as_extension.py
   :language: python
   :lines: 30-33

The :class:`Extension` passed :func:`format_data` is a class defined
by stevedore that wraps the plugin. It includes the name of the
plugin, the :class:`EntryPoint` returned by :mod:`pkg_resources`, and
the plugin itself (the named object referenced by the plugin
definition). When ``invoke_on_load`` is true, the :class:`Extension`
will also have an :attr:`obj` attribute containing the value returned
when the plugin was invoked.

:meth:`map` returns a sequence of the values returned by the callback
function. In this case, :func:`format_data` returns a tuple containing
the extension name and the iterable that produces the text to
print. As the results are processed, the name of each plugin is
printed and then the formatted data.

.. literalinclude:: ../../../stevedore/example/load_as_extension.py
   :language: python
   :lines: 35-39

The order the plugins are loaded is undefined, and depends on the
order packages are found on the import path as well as the way the
metadata files are read. If the order extensions are used matters, try
the :class:`~stevedore.named.NamedExtensionManager`.

.. literalinclude:: extension_output.txt

Why Not Call Plugins Directly?
==============================

Using a separate callable argument to :meth:`map`, rather than just
invoking the plugin directly introduces a separation between your
application code and the plugins. The benefits of this separation
manifest in the application code design and in the plugin API design.

If :meth:`map` called the plugin directly, each plugin would have to
be a callable. That would mean a separate namespace for what is really
just a method of the plugin. By using a separate callable argument,
the plugin API does not need to match exactly any particular use case
in the application. This frees you to create a finer-grained API, with
more individual methods that can be called in different ways to
achieve different goals.

.. seealso::

   * :doc:`/patterns_loading`
   * :doc:`/patterns_enabling`
