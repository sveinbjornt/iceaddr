"""

iceaddr: Look up information about Icelandic streets, addresses,
         placenames, landmarks, locations and postcodes.

Copyright (c) 2018-2025 Sveinbjorn Thordarson.

This file contains code related to placename lookup.

"""

from __future__ import annotations

from typing import Any

from .db import shared_db
from .nearest import find_nearest
from .geo import valid_wgs84_coord

# These particular placenames share a name with other, perhaps larger, placenames,
# but should never the less be given priority when ordering results.
_HARDCODED_PRIORITY = {
    "Hellisheiði": (64.0221268, -21.3413149),  # Nálægt Rvk fær forgang
    "Snæfellsnes": (64.8731746, -23.0309911),  # Nesið norðan við Reykjanes!
    "Mýrdalur": (63.4462885, -19.0832988),  # Nálægt Vík
    "Mosfellsheiði": (64.1675067, -21.3733656),  # Nálægt Mosó
    "Bláfjöll": (64.0121886, -21.5617119),  # Nálægt Rvk á Reykjanesskaga
    "Bakki": (66.0701681, -17.3481556),  # Hjá Húsavík, sbr. verið
    "Bessastaðir": (64.1059036227962, -21.9957549156328),  # Forsetabústaður
    "Gullfoss": (64.3273264, -20.1193949),  # Túrista-áfangastaðurinn fær forgang
    "Grótta": (64.1642163, -22.0218824),  # Á Seltjarnarnesi fær forgang
    "Arnarhóll": (64.147844, -21.9331656),  # Arnarhóll í miðborg Rvk
    "Reykjanes": (63.8185821975681, -22.692991355433815),  # Nesið nálægt Rvk.
}

# This determines the sort order of results
# if there's more than one placename match.
_ORDER = [
    "Dummy",  # Index 0 is reserved for hardcoded priority
    "Sveitarfélag",
    "Þéttbýli",
    "Sveit",
    "Sýsla",
    "Hreppur",
    "Flugvöllur",
    "Jarðgöng",
    "Virkjun",
    "Kirkja",
    "Landörnefni Stórt",
    "Jökla- og snævarörnefni Stórt",
    "Sjávarörnefni Stórt",
    "Vatnaörnefni Stórt",
    "Landörnefni Mið",
    "Jökla- og snævarörnefni Mið",
    "Sjávarörnefni Mið",
    "Vatnaörnefni Mið",
    "Landörnefni Lítið",
    "Jökla- og snævarörnefni Lítið",
    "Sjávarörnefni Lítið",
    "Vatnaörnefni Lítið",
]


def _precedence(pn: dict[str, Any]) -> int:
    """Sort priority for placenames."""
    if pn["nafn"] in _HARDCODED_PRIORITY:
        (lat, lng) = _HARDCODED_PRIORITY[pn["nafn"]]
        if pn["lat_wgs84"] == lat and pn["long_wgs84"] == lng:
            return 0

    fl = pn["flokkur"]
    if fl in _ORDER:
        return _ORDER.index(fl)
    # Any number > len(_ORDER) will do for sorting purposes
    return 9999


def placename_lookup(placename: str, partial: bool = False) -> list[dict[str, Any]]:
    """Look up Icelandic placename in database."""
    q = "SELECT * FROM ornefni WHERE nafn=?"
    if partial:
        q = "SELECT * FROM ornefni WHERE nafn LIKE ?"
        placename = f"%{placename}%"

    db_conn = shared_db.connection()
    res = db_conn.cursor().execute(q, [placename])
    matches = [dict(row) for row in res]
    matches.sort(key=_precedence)

    return matches


def nearest_placenames(
    lat: float, lon: float, limit: int = 1, max_dist: float = 0.0
) -> list[dict[str, Any]]:
    """Find the placename closest to the given coordinates."""

    results_with_dist = nearest_placenames_with_dist(
        lat=lat, lon=lon, limit=limit, max_dist=max_dist
    )

    # Strip out distances for backward compatibility
    return [placename for placename, _dist in results_with_dist]


def nearest_placenames_with_dist(
    lat: float, lon: float, limit: int = 1, max_dist: float = 0.0
) -> list[tuple[dict[str, Any], float]]:
    """Find the placename closest to the given coordinates, with distances.

    Returns a list of tuples where each tuple contains:
    - dict: Placename information
    - float: Distance from the search point in kilometers
    """

    if not valid_wgs84_coord(lat, lon):
        raise ValueError("Invalid latitude or longitude value: {}, {}".format(lat, lon))

    if limit < 0 or max_dist < 0.0:
        raise ValueError("limit and max_dist must be non-negative")

    return find_nearest(
        lat=lat,
        lon=lon,
        rtree_table="ornefni_rtree",
        main_table="ornefni",
        id_column="id",
        limit=limit,
        max_dist=max_dist,
        post_process=None,  # No extra processing needed for placenames
    )
