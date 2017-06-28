====================
 Sphinx Integration
====================

Stevedore includes an extension for integrating with Sphinx to
automatically produce documentation about the supported plugins. To
activate the plugin add ``stevedore.sphinxext`` to the list of
extensions in your ``conf.py``.

.. rst:directive:: .. list-plugins:: namespace

   List the plugins in a namespace.

   Options:

   ``detailed``
      Flag to switch between simple and detailed output (see
      below).
   ``overline-style``
      Character to use to draw line above header,
      defaults to none.
   ``underline-style``
      Character to use to draw line below header,
      defaults to ``=``.

Simple List
===========

By default, the ``list-plugins`` directive produces a simple list of
plugins in a given namespace including the name and the first line of
the docstring. For example:

::

  .. list-plugins:: stevedore.example.formatter

produces

------

.. list-plugins:: stevedore.example.formatter

------

Detailed Lists
==============

Adding the ``detailed`` flag to the directive causes the output to
include a separate subsection for each plugin, with the full docstring
rendered. The section heading level can be controlled using the
``underline-style`` and ``overline-style`` options to fit the results
into the structure of your existing document.

::

  .. list-plugins:: stevedore.example.formatter
     :detailed:

produces

------

.. list-plugins:: stevedore.example.formatter
   :detailed:
   :underline-style: -

------

.. note::

   Depending on how Sphinx is configured, bad reStructuredText syntax in
   the docstrings of the plugins may cause the documentation build to
   fail completely when detailed mode is enabled.
