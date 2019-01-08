# -*- encoding: utf-8 -*-
"""
    iceaddr: Look up information about Icelandic street addresses and postcodes
    Copyright (c) 2018 Sveinbjorn Thordarson
"""

from __future__ import unicode_literals
from __future__ import print_function

import re
from .db import shared_db

HARDCODED_PRIORITY = {
    "Hellisheiði": (64.0221268, -21.3413149),
    "Snæfellsnes": (64.8731746, -23.0309911),
    "Mýrdalur": (63.4462885, -19.0832988),
}

# This determines the sort order of results
# if there's more than one placename match.
ORDER = [
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


def precedence(pn):
    if pn["nafn"] in HARDCODED_PRIORITY:
        (lat, lng) = HARDCODED_PRIORITY[pn["nafn"]]
        if pn["lat_wgs84"] == lat and pn["long_wgs84"] == lng:
            return 0

    fl = pn["flokkur"]
    if fl in ORDER:
        return ORDER.index(fl)
    return 99


def placename_lookup(placename, partial=False):
    q = "SELECT * FROM ornefni WHERE nafn=?"
    if partial:
        q = "SELECT * FROM ornefni WHERE nafn LIKE '?%'"

    db_conn = shared_db.connection()
    res = db_conn.cursor().execute(q, [placename])
    matches = [dict(row) for row in res]
    matches.sort(key=precedence)

    return matches
