# flake8: noqa

from .extension import ExtensionManager
from .enabled import EnabledExtensionManager
from .named import NamedExtensionManager
from .hook import HookManager
from .driver import DriverManager

import logging

# Configure a NullHandler for our log messages in case
# the app we're used from does not set up logging.
LOG = logging.getLogger(__name__)
try:
    LOG.addHandler(logging.NullHandler())
except AttributeError:
    # No NullHandler, probably python 2.6
    pass
