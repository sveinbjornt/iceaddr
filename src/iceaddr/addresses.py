"""

iceaddr: Look up information about Icelandic streets, addresses,
         placenames, landmarks, locations and postcodes.

Copyright (c) 2018-2025 Sveinbjorn Thordarson.

This file contains code related to Icelandic address lookup.

"""

from __future__ import annotations

from typing import Any, Optional

import re

from .db import shared_db
from .geo import valid_wgs84_coord
from .municipalities import MUNICIPALITIES
from .nearest import find_nearest
from .postcodes import POSTCODES, postcodes_for_placename


def _add_postcode_info(addr: dict[str, Any]) -> dict[str, Any]:
    """Look up postcode info, add keys to address dictionary."""
    pn = addr.get("postnr")
    if pn is not None and POSTCODES.get(pn):
        addr.update(POSTCODES[pn])
    return addr


def _add_municipality_info(addr: dict[str, Any]) -> dict[str, Any]:
    """Look up municipality info, add keys to address dictionary."""
    mn = addr.get("svfnr")
    if mn is not None and MUNICIPALITIES.get(mn):
        addr["svfheiti"] = MUNICIPALITIES[mn]
    return addr


def _postprocess_addr(addr: dict[str, Any]) -> dict[str, Any]:
    """Add postcode and municipality info to address."""
    return _add_municipality_info(_add_postcode_info(addr))


def _run_addr_query(q: str, qargs: list[str]) -> list[dict[str, Any]]:
    """Run address query, w. additional postcode data added post hoc."""
    db_conn = shared_db.connection()
    res = db_conn.cursor().execute(q, qargs)
    return [_add_municipality_info(_add_postcode_info(dict(row))) for row in res]


def _cap_first(s: str) -> str:
    """Returns string with first character capitalized. Why this isn't in
    the Python stdlib is beyond me. The capitalize() function annoyingly
    lowercases the rest of the string."""
    return s[:1].upper() + s[1:] if s else s


def iceaddr_lookup(
    street_name: str,
    number: Optional[int] = None,
    letter: Optional[str] = None,
    postcode: Optional[int] = None,
    placename: Optional[str] = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Look up all addresses matching criterion"""

    # Be forgiving, strip and capitalize street name. All street names in DB are capitalized.
    street_name = _cap_first(street_name.strip())

    pc = [postcode] if postcode else []

    # Look up postcodes for placename if no postcode is provided
    if placename and not postcode:
        pc = postcodes_for_placename(placename.strip())
    q = "SELECT * FROM stadfong WHERE"
    name_fields = ["heiti_nf=?", "heiti_tgf=?"]
    if not number:
        # Add lookup for churches and places of interest like Harpa
        name_fields.append("serheiti=?")
    q += "({})".format(" OR ".join(name_fields))
    sqlargs = [street_name] * len(name_fields)

    if number:
        q += " AND (husnr=? OR substr(vidsk, 0, instr(vidsk, '-')) = ?)"
        sqlargs.append(str(number))
        sqlargs.append(str(number))
        if letter:
            q += " AND bokst LIKE ? COLLATE NOCASE"
            sqlargs.append(letter)

    if pc:
        qp = " OR ".join([" postnr=?" for _ in pc])
        sqlargs.extend([str(x) for x in pc])
        q += " AND (%s) " % qp

    # Ordering by postcode may in fact be a reasonable proxy
    # for delivering by order of match likelihood since the
    # lowest postcodes are generally more densely populated
    q += " ORDER BY vidsk != '', postnr ASC, husnr ASC, bokst ASC LIMIT ?"
    sqlargs.append(str(limit))

    return _run_addr_query(q, sqlargs)


MIN_SEARCH_STR_LEN = 3


def iceaddr_suggest(search_str: str, limit: int = 50) -> list[dict[str, Any]]:
    """Parse search string and fetch matching addresses.
    Made to handle partial and full text queries in
    the following formats:

    Öldug
    Öldugata
    Öldugata 4
    Öldugata 4, 101
    Öldugata 4, Reykjavík
    Öldugata 4, 101 Reykjavík
    """

    search_str = _cap_first(search_str.strip())
    if not search_str or len(search_str) < MIN_SEARCH_STR_LEN:
        return []

    items = [s.strip().split() for s in search_str.split(",")]

    if not [a for a in items if len(a)]:
        return []  # Nothing to search for

    # Street name component
    addr = items[0]

    # Handle street names with more than one word, or trailing character
    # E.g. "Stærri Bær 1", "Bárugata 17a"
    if re.match(r"\d+", addr[-1]):
        addr = [" ".join(addr[:-1]), addr[-1]]
        m = re.search(r"([a-zA-Z])$", addr[-1])
        if m:
            addr[-1] = addr[-1][:-1]
            addr.append(m.group(0).lower())
    else:
        addr = [" ".join(addr)]

    q = "SELECT * FROM stadfong WHERE "
    qargs: list[str] = []

    street_name = addr[0]
    if len(addr) == 1:  # "Ölduga"
        q += " (heiti_nf LIKE ? OR heiti_tgf LIKE ?) "
        qargs.extend([street_name + "%", street_name + "%"])
    elif len(addr) >= 2:  # noqa: PLR2004 "Öldugötu 4"
        # Street name
        q += " (heiti_nf=? OR heiti_tgf=?) "
        qargs.extend([street_name, street_name])

        # Street number
        if "-" in addr[1]:
            # "Viðskeyti við staðfang", this is where dashed number ranges are
            q += " AND vidsk=?"
        else:
            q += " AND husnr=?"
        qargs.append(addr[1])

        # Street number's trailing character
        # e.g. if it's "Öldugata 4b"
        if len(addr) == 3:  # noqa: PLR2004
            q += " AND bokst LIKE ? COLLATE NOCASE"
            qargs.append(addr[2])

    # Placename component (postcode or placename)
    if len(items) > 1 and items[1]:
        pns = items[1]
        postcodes: list[str] = []

        # Is it a postcode?
        if re.match(r"\d\d\d$", pns[0]):
            postcodes.append(pns[0])
        else:
            # Try to look up placename
            pc = postcodes_for_placename(pns[0].strip(), partial=True)
            if pc:
                postcodes.extend([str(x) for x in pc])

        if postcodes:
            qp = " OR ".join([" postnr=? " for _ in postcodes])
            q += " AND (%s) " % qp
            qargs.extend(postcodes)

    q += " ORDER BY postnr ASC, husnr ASC, bokst ASC LIMIT ?"
    qargs.append(str(limit))

    return _run_addr_query(q, qargs)


def nearest_addr(
    lat: float, lon: float, limit: int = 1, max_dist: float = 0.0
) -> list[dict[str, Any]]:
    """Find the address closest to the given coordinates."""

    results_with_dist = nearest_addr_with_dist(lat=lat, lon=lon, limit=limit, max_dist=max_dist)

    # Strip out distances for backward compatibility
    return [addr for addr, _dist in results_with_dist]


def nearest_addr_with_dist(
    lat: float, lon: float, limit: int = 1, max_dist: float = 0.0
) -> list[tuple[dict[str, Any], float]]:
    """Find the address closest to the given coordinates, with distances.

    Returns a list of tuples where each tuple contains:
    - dict: Address information with postcode and municipality
    - float: Distance from the search point in kilometers
    """

    if not valid_wgs84_coord(lat, lon):
        raise ValueError("Invalid latitude or longitude value: {}, {}".format(lat, lon))

    if limit < 0 or max_dist < 0.0:
        raise ValueError("limit and max_dist must be non-negative")

    return find_nearest(
        lat=lat,
        lon=lon,
        rtree_table="stadfong_rtree",
        main_table="stadfong",
        id_column="hnitnum",
        limit=limit,
        max_dist=max_dist,
        post_process=_postprocess_addr,
    )
