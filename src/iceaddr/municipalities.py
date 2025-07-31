"""

iceaddr: Look up information about Icelandic streets, addresses,
         placenames, landmarks, locations and postcodes.

Copyright (c) 2018-2025 Sveinbjorn Thordarson.

This file contains code and data related to Icelandic
municipalities (sveitarfélög).

"""

from typing import Optional

MUNICIPALITIES: dict[int, str] = {
    0: "Reykjavíkurborg",
    1000: "Kópavogsbær",
    1100: "Seltjarnarneskaupstaður",
    1300: "Garðabær",
    1400: "Hafnarfjarðarkaupstaður",
    1604: "Mosfellsbær",
    1606: "Kjósarhreppur",
    2000: "Reykjanesbær",
    2300: "Grindavíkurbær",
    2506: "Sveitarfélagið Vogar",
    2510: "Suðurnesjabær",
    3000: "Akraneskaupstaður",
    3506: "Skorradalshreppur",
    3511: "Hvalfjarðarsveit",
    3609: "Borgarbyggð",
    3709: "Grundarfjarðarbær",
    3710: "Helgafellssveit",
    3711: "Stykkishólmsbær",
    3713: "Eyja- og Miklaholtshreppur",
    3714: "Snæfellsbær",
    3811: "Dalabyggð",
    4100: "Bolungarvíkurkaupstaður",
    4200: "Ísafjarðarbær",
    4502: "Reykhólahreppur",
    4604: "Tálknafjarðarhreppur",
    4607: "Vesturbyggð",
    4803: "Súðavíkurhreppur",
    4901: "Árneshreppur",
    4902: "Kaldrananeshreppur",
    4911: "Strandabyggð",
    5200: "Sveitarfélagið Skagafjörður",
    5508: "Húnaþing Vestra",
    5604: "Blönduósbær",
    5609: "Sveitarfélagið Skagaströnd",
    5611: "Skagabyggð",
    5612: "Húnavatnshreppur",
    5706: "Akrahreppur",
    6000: "Akureyrarkaupstaður",
    6100: "Norðurþing",
    6250: "Fjallabyggð",
    6400: "Dalvíkurbyggð",
    6513: "Eyjafjarðarsveit",
    6515: "Hörgársveit",
    6601: "Svalbarðsstrandarhr.",
    6602: "Grýtubakkahreppur",
    6607: "Skútustaðahreppur",
    6611: "Tjörneshreppur",
    6612: "Þingeyjarsveit",
    6706: "Svalbarðshreppur",
    6709: "Langanesbyggð",
    7300: "Fjarðabyggð",
    7502: "Vopnafjarðarhreppur",
    7505: "Fljótsdalshreppur",
    7400: "Múlaþing x",
    7708: "Sveitarfélagið Hornafjörður",
    8000: "Vestmannaeyjabær",
    8200: "Sveitarfélagið Árborg",
    8508: "Mýrdalshreppur",
    8509: "Skaftárhreppur",
    8610: "Ásahreppur",
    8613: "Rangárþing eystra",
    8614: "Rangárþing ytra",
    8710: "Hrunamannahreppur",
    8716: "Hveragerðisbær",
    8717: "Sveitarfélagið Ölfus",
    8719: "Grímsnes- og Grafningshreppur",
    8720: "Skeiða- og Gnúpverjahreppur",
    8721: "Bláskógabyggð",
    8722: "Flóahreppur",
}

# Create a reverse mapping for faster lookups
_NAME_TO_CODE: dict[str, int] = {v: k for k, v in MUNICIPALITIES.items()}


def municipality_for_municipality_code(code: int) -> Optional[str]:
    """Return the name of a municipality given its code."""
    return MUNICIPALITIES.get(code)


def municipality_code_for_municipality(name: str) -> Optional[int]:
    """Return the code of a municipality given its name."""
    return _NAME_TO_CODE.get(name)
