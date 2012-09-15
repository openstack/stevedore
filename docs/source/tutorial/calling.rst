=====================
 Calling the Plugins
=====================

.. explain the args to map()

.. explain why a separate callable is used to combine app & plugin (by
   not passing Ext the callable directly the app use of stevedore does
   not dictate the plugin API, and map() can do more than one thing
   with a plugin
