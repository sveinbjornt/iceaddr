"""

    iceaddr: Look up information about Icelandic streets, addresses,
             placenames, landmarks, locations and postcodes.

    Copyright (c) 2018-2020 Sveinbjorn Thordarson.

    This file contains code related to placename lookup.

"""

import re
from .db import shared_db

HARDCODED_PRIORITY = {
    "Hellisheiði": (64.0221268, -21.3413149),  # Nálægt Rvk fær forgang
    "Snæfellsnes": (64.8731746, -23.0309911),  # Nesið norðan við Reykjanes!
    "Mýrdalur": (63.4462885, -19.0832988),  # Nálægt Vík
    "Mosfellsheiði": (64.1675067, -21.3733656),  # Nálægt Mosó
    "Bláfjöll": (64.0121886, -21.5617119),  # Nálægt Rvk á Reykjanesskaga
    "Bakki": (66.0701681, -17.3481556),  # Hjá Húsavík, sbr. verið
    "Bessastaðir": (64.1059036227962, -21.9957549156328),  # Forsetabústaður
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


def _precedence(pn):
    """ Sort priority for placenames. """
    if pn["nafn"] in HARDCODED_PRIORITY:
        (lat, lng) = HARDCODED_PRIORITY[pn["nafn"]]
        if pn["lat_wgs84"] == lat and pn["long_wgs84"] == lng:
            return 0

    fl = pn["flokkur"]
    if fl in ORDER:
        return ORDER.index(fl)
    return 99


def placename_lookup(placename, partial=False):
    """ Look up Icelandic placename in database. """
    q = "SELECT * FROM ornefni WHERE nafn=?"
    if partial:
        q = "SELECT * FROM ornefni WHERE nafn LIKE '?%'"

    db_conn = shared_db.connection()
    res = db_conn.cursor().execute(q, [placename])
    matches = [dict(row) for row in res]
    matches.sort(key=_precedence)

    return matches
