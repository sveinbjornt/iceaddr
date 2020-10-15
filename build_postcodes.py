#!/usr/bin/env python3
"""

    Fetch list of postcodes from the Icelandic postal service,
    create and print dict mapping postcode to placename and
    other related information. Also adds placenames in the
    nominative case (nefnifall) since the source data only
    includes placenames in dative (þágufall).

    https://www.postur.is/gogn/Gotuskra/postnumer.txt

"""

import requests
from contextlib import closing
import pprint
import logging
import csv
from reynir import NounPhrase

from io import StringIO
from iceaddr.postcodes import POSTCODES

POSTCODES_REMOTE_URL = "https://www.postur.is/gogn/Gotuskra/postnumer.txt"


def read_rows(dsv_file, delimiter="|"):
    reader = csv.DictReader(dsv_file, delimiter=delimiter)
    for row in reader:
        yield row


def _clean_name(name):
    return name.split(" - ")[0].strip()


if __name__ == "__main__":
    pc = dict(POSTCODES)
    pc_keys = pc.keys()
    pp = pprint.PrettyPrinter(indent=4)

    req = requests.get(POSTCODES_REMOTE_URL, allow_redirects=True)
    f = StringIO(req.text)

    changed = False
    reader = csv.DictReader(f, delimiter=";")
    for r in reader:
        # CSV file from postur.is only contains postcode placenames in
        # the dative form (þgf.). Try to lemmatise to nominative (nf.) using Reynir.
        postcode = int(r["Póstnúmer"])
        if postcode not in pc_keys:
            logging.warning(
                "Postcode '{0}' did not already exist in data.".format(postcode)
            )
            changed = True

        tp = r["Tegund"]
        p_dat = _clean_name(r["Staður"])
        p_nom = NounPhrase(p_dat).nominative
        if not p_nom:
            logging.warning("Unable to decline placename '{0}'".format(p_dat))
            p_nom = p_dat

        if pc[postcode]["stadur_nf"] != p_nom:
            pc[postcode]["stadur_nf"] = p_nom
            print("{0} --> {1}".format(pc[postcode]["stadur_nf"], p_nom))
            changed = True

        if pc[postcode]["stadur_tgf"] != p_dat:
            pc[postcode]["stadur_tgf"] = p_dat
            print("{0} --> {1}".format(pc[postcode]["stadur_tgf"], p_dat))
            changed = True

        if pc[postcode]["tegund"] != tp:
            pc[postcode]["tegund"] = tp
            print("{0} --> {1}".format(pc[postcode]["tegund"], tp))
            changed = True

    if not changed:
        print("No change since last update")
    else:
        pp.pprint(pc)
