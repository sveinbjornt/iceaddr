"""

iceaddr: Look up information about Icelandic streets, addresses,
         placenames, landmarks, locations and postcodes.

Copyright (c) 2018-2025 Sveinbjorn Thordarson.

"""

import importlib.metadata

__author__ = "Sveinbjorn Thordarson"
__copyright__ = "(C) 2018-2025 Sveinbjorn Thordarson"
__version__ = importlib.metadata.version("iceaddr")

from .addresses import iceaddr_lookup, iceaddr_suggest, nearest_addr, nearest_addr_with_dist
from .geo import distance, in_iceland
from .meta import iceaddr_metadata
from .municipalities import (
    MUNICIPALITIES,
    municipality_for_municipality_code,
    municipality_code_for_municipality,
)
from .placenames import placename_lookup, nearest_placenames, nearest_placenames_with_dist
from .postcodes import (
    POSTCODES,
    postcode_lookup,
    postcodes_for_region,
    region_for_postcode,
    postcodes_for_placename,
)

__all__ = [
    "iceaddr_lookup",
    "iceaddr_suggest",
    "nearest_addr",
    "nearest_addr_with_dist",
    "distance",
    "in_iceland",
    "iceaddr_metadata",
    "MUNICIPALITIES",
    "municipality_for_municipality_code",
    "municipality_code_for_municipality",
    "placename_lookup",
    "nearest_placenames",
    "nearest_placenames_with_dist",
    "POSTCODES",
    "postcode_lookup",
    "postcodes_for_region",
    "region_for_postcode",
    "postcodes_for_placename",
]
