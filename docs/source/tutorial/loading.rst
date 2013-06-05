=====================
 Loading the Plugins
=====================

Load plugins using stevedore is as easy as creating them. There are
several different enabling and invocation patterns to choose from,
depending on your needs.

Loading Drivers
===============

The most common way plugins are used is as individual drivers. There
may be many plugin options to choose from, but only one needs to be
loaded and called. The :class:`~stevedore.driver.DriverManager` class
supports this pattern.

This example program uses a :class:`DriverManager` to load a formatter
defined in the examples for stevedore. It then uses the formatter to
convert a data structure to a text format, which it can print.

.. literalinclude:: ../../../stevedore/example/load_as_driver.py
   :language: python
   :linenos:
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


.. talk about when to do this, and that it should be done as few times
   as possible (on app startup, rather than on each event)

.. explain invoke_on_load use case


.. seealso::

   * :doc:`/patterns_loading`
   * :doc:`/patterns_enabling`
