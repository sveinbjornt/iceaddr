"""

iceaddr: Look up information about Icelandic streets, addresses,
         placenames, landmarks, locations and postcodes.

Copyright (c) 2018-2025 Sveinbjorn Thordarson.

"""

import importlib.metadata

__author__ = "Sveinbjorn Thordarson"
__copyright__ = "(C) 2018-2025 Sveinbjorn Thordarson"
__version__ = importlib.metadata.version("iceaddr")

from .addresses import *  # noqa: F403
from .municipalities import *  # noqa: F403
from .placenames import *  # noqa: F403
from .postcodes import *  # noqa: F403
