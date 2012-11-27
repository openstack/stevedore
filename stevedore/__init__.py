from .extension import ExtensionManager
from .enabled import EnabledExtensionManager
from .named import NamedExtensionManager
from .hook import HookManager
from .driver import DriverManager

import logging

# Configure a NullHandler for our log messages in case
# the app we're used from does not set up logging.
logging.getLogger(__name__).addHandler(logging.NullHandler())
