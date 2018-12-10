# -*- encoding: utf-8 -*-
"""

    iceaddr: Look up information about Icelandic street addresses and postcodes
    Copyright (c) 2018 Sveinbjorn Thordarson

"""

from __future__ import unicode_literals

postcodes = {
    101: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    103: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    104: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    105: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    107: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    108: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    109: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    110: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    111: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    112: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    113: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    116: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Þéttbýli",
    },
    121: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Pósthólf",
    },
    123: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Pósthólf",
    },
    124: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Pósthólf",
    },
    125: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Pósthólf",
    },
    127: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Pósthólf",
    },
    128: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Pósthólf",
    },
    129: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Pósthólf",
    },
    130: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Pósthólf",
    },
    132: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík",
        "tegund": "Pósthólf",
    },
    162: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Reykjavík",
        "stadur_tgf": "Reykjavík - Dreifbýli",
        "tegund": "Dreifbýli",
    },
    170: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Seltjarnarnes",
        "stadur_tgf": "Seltjarnarnesi",
        "tegund": "Þéttbýli",
    },
    172: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Seltjarnarnes",
        "stadur_tgf": "Seltjarnarnesi",
        "tegund": "Pósthólf",
    },
    190: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Vogar",
        "stadur_tgf": "Vogum",
        "tegund": "Þéttbýli",
    },
    191: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Vogar",
        "stadur_tgf": "Vogum",
        "tegund": "Dreifbýli",
    },
    200: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Kópavogur",
        "stadur_tgf": "Kópavogi",
        "tegund": "Þéttbýli",
    },
    201: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Kópavogur",
        "stadur_tgf": "Kópavogi",
        "tegund": "Þéttbýli",
    },
    202: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Kópavogur",
        "stadur_tgf": "Kópavogi",
        "tegund": "Pósthólf",
    },
    203: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Kópavogur",
        "stadur_tgf": "Kópavogi",
        "tegund": "Þéttbýli",
    },
    210: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Garðabær",
        "stadur_tgf": "Garðabæ",
        "tegund": "Þéttbýli",
    },
    212: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Garðabær",
        "stadur_tgf": "Garðabæ",
        "tegund": "Pósthólf",
    },
    220: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Hafnarfjörður",
        "stadur_tgf": "Hafnarfirði",
        "tegund": "Þéttbýli",
    },
    221: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Hafnarfjörður",
        "stadur_tgf": "Hafnarfirði",
        "tegund": "Þéttbýli",
    },
    222: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Hafnarfjörður",
        "stadur_tgf": "Hafnarfirði",
        "tegund": "Pósthólf",
    },
    225: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Garðabær",
        "stadur_tgf": "Garðabær",
        "tegund": "Þéttbýli",
    },
    230: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Reykjanesbær",
        "stadur_tgf": "Reykjanesbæ",
        "tegund": "Þéttbýli",
    },
    232: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Reykjanesbær",
        "stadur_tgf": "Reykjanesbæ",
        "tegund": "Pósthólf",
    },
    233: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Reykjanesbær",
        "stadur_tgf": "Reykjanesbæ",
        "tegund": "Dreifbýli",
    },
    235: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Keflavíkurflugvöllur",
        "stadur_tgf": "Keflavíkurflugvöllur",
        "tegund": "Þéttbýli",
    },
    240: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Grindavík",
        "stadur_tgf": "Grindavík",
        "tegund": "Þéttbýli",
    },
    241: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Grindavík",
        "stadur_tgf": "Grindavík",
        "tegund": "Dreifbýli",
    },
    245: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Sandgerði",
        "stadur_tgf": "Sandgerði",
        "tegund": "Þéttbýli",
    },
    246: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Sandgerði",
        "stadur_tgf": "Sandgerði",
        "tegund": "Dreifbýli",
    },
    250: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Garður",
        "stadur_tgf": "Garði",
        "tegund": "Þéttbýli",
    },
    251: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Garður",
        "stadur_tgf": "Garði",
        "tegund": "Dreifbýli",
    },
    260: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Reykjanesbær",
        "stadur_tgf": "Reykjanesbæ",
        "tegund": "Þéttbýli",
    },
    262: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Reykjanesbær",
        "stadur_tgf": "Reykjanesbæ",
        "tegund": "Þéttbýli",
    },
    270: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Mosfellsbær",
        "stadur_tgf": "Mosfellsbæ",
        "tegund": "Þéttbýli",
    },
    271: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Mosfellsbær",
        "stadur_tgf": "Mosfellsbæ",
        "tegund": "Dreifbýli",
    },
    276: {
        "svaedi": "Höfuðborgarsvæðið",
        "stadur_nf": "Mosfellsbær",
        "stadur_tgf": "Mosfellsbæ",
        "tegund": "Dreifbýli",
    },
    300: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Akranes",
        "stadur_tgf": "Akranesi",
        "tegund": "Þéttbýli",
    },
    301: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Akranes",
        "stadur_tgf": "Akranesi",
        "tegund": "Dreifbýli",
    },
    302: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Akranes",
        "stadur_tgf": "Akranesi",
        "tegund": "Pósthólf",
    },
    310: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Borgarnes",
        "stadur_tgf": "Borgarnesi",
        "tegund": "Þéttbýli",
    },
    311: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Borgarnes",
        "stadur_tgf": "Borgarnesi",
        "tegund": "Dreifbýli",
    },
    320: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Reykholt í Borgarfirði",
        "stadur_tgf": "Reykholt í Borgarfirði",
        "tegund": "Dreifbýli",
    },
    340: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Stykkishólmur",
        "stadur_tgf": "Stykkishólmi",
        "tegund": "Þéttbýli",
    },
    341: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Stykkishólmur",
        "stadur_tgf": "Stykkishólmi",
        "tegund": "Dreifbýli",
    },
    345: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Flatey á Breiðafirði",
        "stadur_tgf": "Flatey á Breiðafirði",
        "tegund": "Dreifbýli",
    },
    350: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Grundarfjörður",
        "stadur_tgf": "Grundarfirði",
        "tegund": "Þéttbýli",
    },
    351: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Grundarfjörður",
        "stadur_tgf": "Grundarfirði",
        "tegund": "Dreifbýli",
    },
    355: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Ólafsvík",
        "stadur_tgf": "Ólafsvík",
        "tegund": "Þéttbýli",
    },
    356: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Snæfellsbær",
        "stadur_tgf": "Snæfellsbæ",
        "tegund": "Dreifbýli",
    },
    360: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Hellissandur",
        "stadur_tgf": "Hellissandi",
        "tegund": "Þéttbýli",
    },
    370: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Búðardalur",
        "stadur_tgf": "Búðardal",
        "tegund": "Þéttbýli",
    },
    371: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Búðardalur",
        "stadur_tgf": "Búðardal",
        "tegund": "Dreifbýli",
    },
    380: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Reykhólahreppur",
        "stadur_tgf": "Reykhólahreppi",
        "tegund": "Þéttbýli",
    },
    381: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Reykhólahreppur",
        "stadur_tgf": "Reykhólahreppi",
        "tegund": "Dreifbýli",
    },
    400: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Ísafjörður",
        "stadur_tgf": "Ísafirði",
        "tegund": "Þéttbýli",
    },
    401: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Ísafjörður",
        "stadur_tgf": "Ísafirði",
        "tegund": "Dreifbýli",
    },
    410: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Hnífsdalur",
        "stadur_tgf": "Hnífsdal",
        "tegund": "Þéttbýli",
    },
    415: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Bolungarvík",
        "stadur_tgf": "Bolungarvík",
        "tegund": "Þéttbýli",
    },
    416: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Bolungarvík",
        "stadur_tgf": "Bolungarvík",
        "tegund": "Dreifbýli",
    },
    420: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Súðavík",
        "stadur_tgf": "Súðavík",
        "tegund": "Þéttbýli",
    },
    421: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Súðavík",
        "stadur_tgf": "Súðavík",
        "tegund": "Dreifbýli",
    },
    425: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Flateyri",
        "stadur_tgf": "Flateyri",
        "tegund": "Þéttbýli",
    },
    426: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Flateyri",
        "stadur_tgf": "Flateyri",
        "tegund": "Dreifbýli",
    },
    430: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Suðureyri",
        "stadur_tgf": "Suðureyri",
        "tegund": "Þéttbýli",
    },
    431: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Suðureyri",
        "stadur_tgf": "Suðureyri",
        "tegund": "Dreifbýli",
    },
    450: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Patreksfjörður",
        "stadur_tgf": "Patreksfirði",
        "tegund": "Þéttbýli",
    },
    451: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Patreksfjörður",
        "stadur_tgf": "Patreksfirði",
        "tegund": "Dreifbýli",
    },
    460: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Tálknafjörður",
        "stadur_tgf": "Tálknafirði",
        "tegund": "Þéttbýli",
    },
    461: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Tálknafjörður",
        "stadur_tgf": "Tálknafirði",
        "tegund": "Dreifbýli",
    },
    465: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Bíldudalur",
        "stadur_tgf": "Bíldudal",
        "tegund": "Þéttbýli",
    },
    466: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Bíldudalur",
        "stadur_tgf": "Bíldudal",
        "tegund": "Dreifbýli",
    },
    470: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Þingeyri",
        "stadur_tgf": "Þingeyri",
        "tegund": "Þéttbýli",
    },
    471: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Þingeyri",
        "stadur_tgf": "Þingeyri",
        "tegund": "Dreifbýli",
    },
    500: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Staður",
        "stadur_tgf": "Stað",
        "tegund": "Dreifbýli",
    },
    510: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Hólmavík",
        "stadur_tgf": "Hólmavík",
        "tegund": "Þéttbýli",
    },
    511: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Hólmavík",
        "stadur_tgf": "Hólmavík",
        "tegund": "Dreifbýli",
    },
    512: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Hólmavík",
        "stadur_tgf": "Hólmavík",
        "tegund": "Dreifbýli",
    },
    520: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Drangsnes",
        "stadur_tgf": "Drangsnesi",
        "tegund": "Þéttbýli",
    },
    524: {
        "svaedi": "Vesturland og Vestfirðir",
        "stadur_nf": "Árneshreppur",
        "stadur_tgf": "Árneshreppi",
        "tegund": "Dreifbýli",
    },
    530: {
        "svaedi": "Norðurland",
        "stadur_nf": "Hvammstangi",
        "stadur_tgf": "Hvammstanga",
        "tegund": "Þéttbýli",
    },
    531: {
        "svaedi": "Norðurland",
        "stadur_nf": "Hvammstangi",
        "stadur_tgf": "Hvammstanga",
        "tegund": "Dreifbýli",
    },
    540: {
        "svaedi": "Norðurland",
        "stadur_nf": "Blönduós",
        "stadur_tgf": "Blönduósi",
        "tegund": "Þéttbýli",
    },
    541: {
        "svaedi": "Norðurland",
        "stadur_nf": "Blönduós",
        "stadur_tgf": "Blönduósi",
        "tegund": "Dreifbýli",
    },
    545: {
        "svaedi": "Norðurland",
        "stadur_nf": "Skagaströnd",
        "stadur_tgf": "Skagaströnd",
        "tegund": "Þéttbýli",
    },
    546: {
        "svaedi": "Norðurland",
        "stadur_nf": "Skagaströnd",
        "stadur_tgf": "Skagaströnd",
        "tegund": "Dreifbýli",
    },
    550: {
        "svaedi": "Norðurland",
        "stadur_nf": "Sauðárkrókur",
        "stadur_tgf": "Sauðárkróki",
        "tegund": "Þéttbýli",
    },
    551: {
        "svaedi": "Norðurland",
        "stadur_nf": "Sauðárkrókur",
        "stadur_tgf": "Sauðárkróki",
        "tegund": "Dreifbýli",
    },
    560: {
        "svaedi": "Norðurland",
        "stadur_nf": "Varmahlíð",
        "stadur_tgf": "Varmahlíð",
        "tegund": "Þéttbýli",
    },
    561: {
        "svaedi": "Norðurland",
        "stadur_nf": "Varmahlíð",
        "stadur_tgf": "Varmahlíð",
        "tegund": "Dreifbýli",
    },
    565: {
        "svaedi": "Norðurland",
        "stadur_nf": "Hofsós",
        "stadur_tgf": "Hofsós",
        "tegund": "Þéttbýli",
    },
    566: {
        "svaedi": "Norðurland",
        "stadur_nf": "Hofsós",
        "stadur_tgf": "Hofsós",
        "tegund": "Dreifbýli",
    },
    570: {
        "svaedi": "Norðurland",
        "stadur_nf": "Fljót",
        "stadur_tgf": "Fljótum",
        "tegund": "Dreifbýli",
    },
    580: {
        "svaedi": "Norðurland",
        "stadur_nf": "Siglufjörður",
        "stadur_tgf": "Siglufirði",
        "tegund": "Þéttbýli",
    },
    581: {
        "svaedi": "Norðurland",
        "stadur_nf": "Siglufjörður",
        "stadur_tgf": "Siglufirði",
        "tegund": "Dreifbýli",
    },
    600: {
        "svaedi": "Norðurland",
        "stadur_nf": "Akureyri",
        "stadur_tgf": "Akureyri",
        "tegund": "Þéttbýli",
    },
    601: {
        "svaedi": "Norðurland",
        "stadur_nf": "Akureyri",
        "stadur_tgf": "Akureyri",
        "tegund": "Dreifbýli",
    },
    602: {
        "svaedi": "Norðurland",
        "stadur_nf": "Akureyri",
        "stadur_tgf": "Akureyri",
        "tegund": "Pósthólf",
    },
    603: {
        "svaedi": "Norðurland",
        "stadur_nf": "Akureyri",
        "stadur_tgf": "Akureyri",
        "tegund": "Þéttbýli",
    },
    610: {
        "svaedi": "Norðurland",
        "stadur_nf": "Grenivík",
        "stadur_tgf": "Grenivík",
        "tegund": "Þéttbýli",
    },
    611: {
        "svaedi": "Norðurland",
        "stadur_nf": "Grímsey",
        "stadur_tgf": "Grímsey",
        "tegund": "Þéttbýli",
    },
    616: {
        "svaedi": "Norðurland",
        "stadur_nf": "Grenivík",
        "stadur_tgf": "Grenivík",
        "tegund": "Dreifbýli",
    },
    620: {
        "svaedi": "Norðurland",
        "stadur_nf": "Dalvík",
        "stadur_tgf": "Dalvík",
        "tegund": "Þéttbýli",
    },
    621: {
        "svaedi": "Norðurland",
        "stadur_nf": "Dalvík",
        "stadur_tgf": "Dalvík",
        "tegund": "Dreifbýli",
    },
    625: {
        "svaedi": "Norðurland",
        "stadur_nf": "Ólafsfjörður",
        "stadur_tgf": "Ólafsfirði",
        "tegund": "Þéttbýli",
    },
    626: {
        "svaedi": "Norðurland",
        "stadur_nf": "Ólafsfjörður",
        "stadur_tgf": "Ólafsfirði",
        "tegund": "Dreifbýli",
    },
    630: {
        "svaedi": "Norðurland",
        "stadur_nf": "Hrísey",
        "stadur_tgf": "Hrísey",
        "tegund": "Þéttbýli",
    },
    640: {
        "svaedi": "Norðurland",
        "stadur_nf": "Húsavík",
        "stadur_tgf": "Húsavík",
        "tegund": "Þéttbýli",
    },
    641: {
        "svaedi": "Norðurland",
        "stadur_nf": "Húsavík",
        "stadur_tgf": "Húsavík",
        "tegund": "Dreifbýli",
    },
    645: {
        "svaedi": "Norðurland",
        "stadur_nf": "Fosshólli",
        "stadur_tgf": "Fosshólli",
        "tegund": "Dreifbýli",
    },
    650: {
        "svaedi": "Norðurland",
        "stadur_nf": "Laugar",
        "stadur_tgf": "Laugum",
        "tegund": "Þéttbýli",
    },
    660: {
        "svaedi": "Norðurland",
        "stadur_nf": "Mývatn",
        "stadur_tgf": "Mývatni",
        "tegund": "Dreifbýli",
    },
    670: {
        "svaedi": "Norðurland",
        "stadur_nf": "Kópasker",
        "stadur_tgf": "Kópaskeri",
        "tegund": "Þéttbýli",
    },
    671: {
        "svaedi": "Norðurland",
        "stadur_nf": "Kópasker",
        "stadur_tgf": "Kópaskeri",
        "tegund": "Dreifbýli",
    },
    675: {
        "svaedi": "Norðurland",
        "stadur_nf": "Raufarhöfn",
        "stadur_tgf": "Raufarhöfn",
        "tegund": "Þéttbýli",
    },
    676: {
        "svaedi": "Norðurland",
        "stadur_nf": "Raufarhöfn",
        "stadur_tgf": "Raufarhöfn",
        "tegund": "Dreifbýli",
    },
    680: {
        "svaedi": "Norðurland",
        "stadur_nf": "Þórshöfn",
        "stadur_tgf": "Þórshöfn",
        "tegund": "Þéttbýli",
    },
    681: {
        "svaedi": "Norðurland",
        "stadur_nf": "Þórshöfn",
        "stadur_tgf": "Þórshöfn",
        "tegund": "Dreifbýli",
    },
    685: {
        "svaedi": "Norðurland",
        "stadur_nf": "Bakkafjörður",
        "stadur_tgf": "Bakkafirði",
        "tegund": "Þéttbýli",
    },
    686: {
        "svaedi": "Norðurland",
        "stadur_nf": "Bakkafjörður",
        "stadur_tgf": "Bakkafirði",
        "tegund": "Dreifbýli",
    },
    690: {
        "svaedi": "Norðurland",
        "stadur_nf": "Vopnafjörður",
        "stadur_tgf": "Vopnafirði",
        "tegund": "Þéttbýli",
    },
    691: {
        "svaedi": "Norðurland",
        "stadur_nf": "Vopnafjörður",
        "stadur_tgf": "Vopnafirði",
        "tegund": "Dreifbýli",
    },
    700: {
        "svaedi": "Austurland",
        "stadur_nf": "Egilsstaðir",
        "stadur_tgf": "Egilsstöðum",
        "tegund": "Þéttbýli",
    },
    701: {
        "svaedi": "Austurland",
        "stadur_nf": "Egilsstaðir",
        "stadur_tgf": "Egilsstöðum",
        "tegund": "Dreifbýli",
    },
    710: {
        "svaedi": "Austurland",
        "stadur_nf": "Seyðisfjörður",
        "stadur_tgf": "Seyðisfirði",
        "tegund": "Þéttbýli",
    },
    711: {
        "svaedi": "Austurland",
        "stadur_nf": "Seyðisfjörður",
        "stadur_tgf": "Seyðisfirði",
        "tegund": "Dreifbýli",
    },
    715: {
        "svaedi": "Austurland",
        "stadur_nf": "Mjóifjörður",
        "stadur_tgf": "Mjóafirði",
        "tegund": "Dreifbýli",
    },
    720: {
        "svaedi": "Austurland",
        "stadur_nf": "Borgarfjörður",
        "stadur_tgf": "Borgarfirði (eystri)",
        "tegund": "Dreifbýli",
    },
    721: {
        "svaedi": "Austurland",
        "stadur_nf": "Borgarfjörður",
        "stadur_tgf": "Borgarfirði (eystri)",
        "tegund": "Dreifbýli",
    },
    730: {
        "svaedi": "Austurland",
        "stadur_nf": "Reyðarfjörður",
        "stadur_tgf": "Reyðarfirði",
        "tegund": "Þéttbýli",
    },
    731: {
        "svaedi": "Austurland",
        "stadur_nf": "Reyðarfjörður",
        "stadur_tgf": "Reyðarfirði",
        "tegund": "Dreifbýli",
    },
    735: {
        "svaedi": "Austurland",
        "stadur_nf": "Eskifjörður",
        "stadur_tgf": "Eskifirði",
        "tegund": "Þéttbýli",
    },
    736: {
        "svaedi": "Austurland",
        "stadur_nf": "Eskifjörður",
        "stadur_tgf": "Eskifirði",
        "tegund": "Dreifbýli",
    },
    740: {
        "svaedi": "Austurland",
        "stadur_nf": "Neskaupstaður",
        "stadur_tgf": "Neskaupstað",
        "tegund": "Þéttbýli",
    },
    741: {
        "svaedi": "Austurland",
        "stadur_nf": "Neskaupsstaður",
        "stadur_tgf": "Neskaupsstað",
        "tegund": "Dreifbýli",
    },
    750: {
        "svaedi": "Austurland",
        "stadur_nf": "Fáskrúðsfjörður",
        "stadur_tgf": "Fáskrúðsfirði",
        "tegund": "Þéttbýli",
    },
    751: {
        "svaedi": "Austurland",
        "stadur_nf": "Fáskrúðsfjörður",
        "stadur_tgf": "Fáskrúðsfirði",
        "tegund": "Dreifbýli",
    },
    755: {
        "svaedi": "Austurland",
        "stadur_nf": "Stöðvarfjörður",
        "stadur_tgf": "Stöðvarfirði",
        "tegund": "Þéttbýli",
    },
    756: {
        "svaedi": "Austurland",
        "stadur_nf": "Stöðvarfjörður",
        "stadur_tgf": "Stöðvarfirði",
        "tegund": "Dreifbýli",
    },
    760: {
        "svaedi": "Austurland",
        "stadur_nf": "Breiðdalsvík",
        "stadur_tgf": "Breiðdalsvík",
        "tegund": "Þéttbýli",
    },
    761: {
        "svaedi": "Austurland",
        "stadur_nf": "Breiðdalsvík",
        "stadur_tgf": "Breiðdalsvík",
        "tegund": "Dreifbýli",
    },
    765: {
        "svaedi": "Austurland",
        "stadur_nf": "Djúpivogur",
        "stadur_tgf": "Djúpavogi",
        "tegund": "Þéttbýli",
    },
    766: {
        "svaedi": "Austurland",
        "stadur_nf": "Djúpivogur",
        "stadur_tgf": "Djúpavogi",
        "tegund": "Dreifbýli",
    },
    780: {
        "svaedi": "Austurland",
        "stadur_nf": "Höfn í Hornafirði",
        "stadur_tgf": "Höfn í Hornafirði",
        "tegund": "Þéttbýli",
    },
    781: {
        "svaedi": "Austurland",
        "stadur_nf": "Höfn í Hornafirði",
        "stadur_tgf": "Höfn í Hornafirði",
        "tegund": "Dreifbýli",
    },
    785: {
        "svaedi": "Austurland",
        "stadur_nf": "Öræfi",
        "stadur_tgf": "Öræfum",
        "tegund": "Dreifbýli",
    },
    800: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Selfoss",
        "stadur_tgf": "Selfossi",
        "tegund": "Þéttbýli",
    },
    801: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Selfoss",
        "stadur_tgf": "Selfossi",
        "tegund": "Dreifbýli",
    },
    802: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Selfoss",
        "stadur_tgf": "Selfossi",
        "tegund": "Pósthólf",
    },
    810: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Hveragerði",
        "stadur_tgf": "Hveragerði",
        "tegund": "Þéttbýli",
    },
    815: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Þorlákshöfn",
        "stadur_tgf": "Þorlákshöfn",
        "tegund": "Þéttbýli",
    },
    816: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Ölfus",
        "stadur_tgf": "Ölfus",
        "tegund": "Dreifbýli",
    },
    820: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Eyrarbakki",
        "stadur_tgf": "Eyrarbakka",
        "tegund": "Þéttbýli",
    },
    825: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Stokkseyri",
        "stadur_tgf": "Stokkseyri",
        "tegund": "Þéttbýli",
    },
    840: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Laugarvatn",
        "stadur_tgf": "Laugarvatni",
        "tegund": "Þéttbýli",
    },
    845: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Flúðir",
        "stadur_tgf": "Flúðum",
        "tegund": "Þéttbýli",
    },
    846: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Flúðir",
        "stadur_tgf": "Flúðum",
        "tegund": "Dreifbýli",
    },
    850: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Hella",
        "stadur_tgf": "Hellu",
        "tegund": "Þéttbýli",
    },
    851: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Hella",
        "stadur_tgf": "Hellu",
        "tegund": "Dreifbýli",
    },
    860: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Hvolsvöllur",
        "stadur_tgf": "Hvolsvelli",
        "tegund": "Þéttbýli",
    },
    861: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Hvolsvöllur",
        "stadur_tgf": "Hvolsvelli",
        "tegund": "Dreifbýli",
    },
    870: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Vík",
        "stadur_tgf": "Vík",
        "tegund": "Þéttbýli",
    },
    871: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Vík",
        "stadur_tgf": "Vík",
        "tegund": "Dreifbýli",
    },
    880: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Kirkjubæjarklaustur",
        "stadur_tgf": "Kirkjubæjarklaustri",
        "tegund": "Þéttbýli",
    },
    881: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Kirkjubæjarklaustur",
        "stadur_tgf": "Kirkjubæjarklaustri",
        "tegund": "Dreifbýli",
    },
    900: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Vestmannaeyjar",
        "stadur_tgf": "Vestmannaeyjum",
        "tegund": "Þéttbýli",
    },
    902: {
        "svaedi": "Suðurland og Reykjanes",
        "stadur_nf": "Vestmannaeyjar",
        "stadur_tgf": "Vestmannaeyjum",
        "tegund": "Pósthólf",
    },
}


def postcodes_for_placename(pn, partial=False):
    p = pn.lower()
    matches = list()

    for k, v in postcodes.items():
        nf = v["stadur_nf"].lower()
        tgf = v["stadur_tgf"].lower()
        if partial and (nf.startswith(p) or tgf.startswith(p)):
            matches.append(k)
        elif nf == p or tgf == p:
            matches.append(k)

    return matches
