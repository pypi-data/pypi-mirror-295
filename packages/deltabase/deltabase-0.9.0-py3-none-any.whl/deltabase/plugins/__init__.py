
from logging import getLogger

debugger = getLogger("deltabase.plugin.salesforce")

from .base import delta_plugin

try: from .salesforce import salesforce
except ImportError:
    debugger.info("unable to load salesforce plugin. `deltabase[salesforce]` package required.")