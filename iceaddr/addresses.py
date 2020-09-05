"""

    iceaddr: Look up information about Icelandic streets, addresses,
             placenames, landmarks, locations and postcodes.

    Copyright (c) 2018-2020 Sveinbjorn Thordarson.

    This file contains code related to Icelandic address lookup.

"""

import re

from .db import shared_db
from .postcodes import POSTCODES, postcodes_for_placename
from .dist import distance


def _add_postcode_info(addr):
    """ Look up postcode info, add keys to address dictionary. """
    pn = addr.get("postnr")
    if pn and POSTCODES.get(pn):
        addr.update(POSTCODES[pn])
    return addr


def _run_addr_query(q, qargs):
    """ Run address query, w. additional postcode data added post hoc. """
    db_conn = shared_db.connection()
    res = db_conn.cursor().execute(q, qargs)
    return [_add_postcode_info(dict(row)) for row in res]


def _cap_first(s):
    """ Returns string with first character capitalized. Why this isn't in
        the Python stdlib is beyond me. The capitalize() function annoyingly
        lowercases the rest of the string. """
    return s[:1].upper() + s[1:] if s else s


def iceaddr_lookup(
    street_name, number=None, letter=None, postcode=None, placename=None, limit=50
):
    """ Look up all addresses matching criterion """

    # Be forgivin, strip and capitalize street name. Al street names in DB are cpitalized.
    street_name = _cap_first(street_name.strip())

    pc = [postcode] if postcode else []

    # Look up postcodes for placename if no postcode is provided
    if placename and not postcode:
        pc = postcodes_for_placename(placename.strip())

    q = "SELECT * FROM stadfong WHERE (heiti_nf=? OR heiti_tgf=?)"
    sqlargs = [street_name, street_name]
    if number:
        q += " AND husnr=? "
        sqlargs.append(number)
        if letter:
            q += " AND bokst LIKE ? COLLATE NOCASE"
            sqlargs.append(letter)
    if pc:
        qp = " OR ".join([" postnr=?" for p in pc])
        sqlargs.extend(pc)
        q += " AND (%s) " % qp

    # Ordering by postcode may in fact be a reasonable proxy
    # for delivering by order of match likelihood since the
    # lowest postcodes are generally more densely populated
    q += " ORDER BY postnr ASC, husnr ASC, bokst ASC LIMIT ?"
    sqlargs.append(limit)

    return _run_addr_query(q, sqlargs)


def iceaddr_suggest(search_str, limit=50):
    """ Parse search string and fetch matching addresses.
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
    if not search_str or len(search_str) < 3:
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
    qargs = list()

    street_name = addr[0]
    if len(addr) == 1:  # "Ölduga"
        q += " (heiti_nf LIKE ? OR heiti_tgf LIKE ?) "
        qargs.extend([street_name + "%", street_name + "%"])
    elif len(addr) >= 2:  # "Öldugötu 4"
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
        if len(addr) == 3:
            q += " AND bokst LIKE ? COLLATE NOCASE"
            qargs.append(addr[2])

    # Placename component (postcode or placename)
    if len(items) > 1 and items[1]:
        pns = items[1]
        postcodes = []

        # Is it a postcode?
        if re.match(r"\d\d\d$", pns[0]):
            postcodes.append(pns[0])
        else:
            # Try to look up placename
            pc = postcodes_for_placename(pns[0].strip(), partial=True)
            if pc:
                postcodes.extend(pc)

        if postcodes:
            qp = " OR ".join([" postnr=? " for p in postcodes])
            q += " AND (%s) " % qp
            qargs.extend(postcodes)

    q += " ORDER BY postnr ASC, husnr ASC, bokst ASC LIMIT ?"
    qargs.append(limit)

    return _run_addr_query(q, qargs)


def nearest_addr(lat, lon, limit=1):
    """ Find the address closest to the given coordinates. """
    q = "SELECT * FROM stadfong"
    db_conn = shared_db.connection()
    res = db_conn.cursor().execute(q, [])
    closest = sorted(
        res, key=lambda i: distance((lat, lon), (i["lat_wgs84"], i["long_wgs84"]))
    )
    return [_add_postcode_info(x) for x in closest[:limit]]
