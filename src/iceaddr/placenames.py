"""

iceaddr: Look up information about Icelandic streets, addresses,
         placenames, landmarks, locations and postcodes.

Copyright (c) 2018-2026 Sveinbjorn Thordarson.

This file contains code related to placename lookup.

"""

from __future__ import annotations

from typing import Any

from .db import shared_db
from .nearest import find_nearest
from .geo import distance, valid_wgs84_coord

# These particular placenames share a name with other, perhaps larger, placenames,
# but should never the less be given priority when ordering results. The coordinates
# identify which row to prioritise. They are matched with a tolerance rather than
# exactly (see _PRIORITY_MATCH_RADIUS_KM) because the source data nudges coordinates
# around slightly every time the placename dataset is regenerated.
_HARDCODED_PRIORITY = {
    "Hellisheiði": (64.0221245213045, -21.34131414063142),  # Nálægt Rvk fær forgang
    "Snæfellsnes": (64.87836446028145, -23.066074272626825),  # Nesið norðan við Reykjanes!
    "Mýrdalur": (63.37571287874832, -19.097060864382204),  # Sveitin hjá Vík
    "Mosfellsheiði": (64.16749528868228, -21.3733545290797),  # Nálægt Mosó
    "Bláfjöll": (64.01217735661965, -21.56167096053218),  # Nálægt Rvk á Reykjanesskaga
    "Bakki": (66.07024989087778, -17.343971270338788),  # Hjá Húsavík, sbr. verið
    "Bessastaðir": (64.1059036227962, -21.9957549156328),  # Forsetabústaður
    "Gullfoss": (64.32732642193642, -20.119394921580646),  # Túrista-áfangastaðurinn fær forgang
    "Grótta": (64.16421625171155, -22.021882426691786),  # Á Seltjarnarnesi fær forgang
    "Arnarhóll": (64.14784396321001, -21.933165599564227),  # Arnarhóll í miðborg Rvk
    "Reykjanes": (63.8185821975681, -22.692991355433815),  # Nesið nálægt Rvk.
}

# How far a placename row may sit from its hardcoded coordinate and still be
# considered the intended one. Comfortably larger than the drift seen between
# releases of the source data, and comfortably smaller than the distance to the
# nearest rival placename of the same name (~10 km at the tightest).
_PRIORITY_MATCH_RADIUS_KM = 5.0

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
    """Sort priority for placenames, based on the kind of place it is."""
    fl = pn["flokkur"]
    if fl in _ORDER:
        return _ORDER.index(fl)
    # Any number > len(_ORDER) will do for sorting purposes
    return 9999


def _hardcoded_priority_ids(matches: list[dict[str, Any]]) -> set[int]:
    """Find the rows that the hardcoded priority coordinates point at.

    For each name in _HARDCODED_PRIORITY, the closest row within
    _PRIORITY_MATCH_RADIUS_KM of the hardcoded coordinate wins.
    """
    closest: dict[str, tuple[float, int]] = {}

    for pn in matches:
        coords = _HARDCODED_PRIORITY.get(pn["nafn"])
        if coords is None:
            continue
        d = distance(coords, (pn["lat_wgs84"], pn["long_wgs84"]))
        if d > _PRIORITY_MATCH_RADIUS_KM:
            continue
        prev = closest.get(pn["nafn"])
        if prev is None or d < prev[0]:
            closest[pn["nafn"]] = (d, pn["id"])

    return {pn_id for _, pn_id in closest.values()}


def placename_lookup(placename: str, partial: bool = False) -> list[dict[str, Any]]:
    """Look up Icelandic placename in database."""
    q = "SELECT * FROM ornefni WHERE nafn=?"
    if partial:
        q = "SELECT * FROM ornefni WHERE nafn LIKE ?"
        placename = f"%{placename}%"

    db_conn = shared_db.connection()
    res = db_conn.cursor().execute(q, [placename])
    matches = [dict(row) for row in res]

    # Index 0 of _ORDER is reserved for the hardcoded priority rows
    prioritized = _hardcoded_priority_ids(matches)
    matches.sort(key=lambda pn: 0 if pn["id"] in prioritized else _precedence(pn))

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
