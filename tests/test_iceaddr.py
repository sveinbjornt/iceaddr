"""

    test_iceaddr.py

    Tests for iceaddr package
    
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../")

from iceaddr import iceaddr_lookup, iceaddr_suggest, postcodes_for_placename


def test_address_lookup():
    ADDR_TO_POSTCODE = [
        ["Öldugata", 4, "Reykjavík", 101],
        ["öldugötu", 12, "hafnarfirði", 220],
        ["Tómasarhaga", 12, "Reykjavík", 107],
        ["smiðjuvegur", 22, None, 200],
    ]

    for a in ADDR_TO_POSTCODE:
        res = iceaddr_lookup(a[0], number=a[1], placename=a[2])
        assert res[0]["postnr"] == a[3]

    res = iceaddr_lookup("Brattagata", number=4, letter="b")
    assert res and res[0]["postnr"] == 310 and res[0]["stadur_nf"] == "Borgarnes"

    POSTCODE_TO_PLACENAME = [
        ["Öldugata", 4, 101, "Reykjavík", "Höfuðborgarsvæðið", "Þéttbýli"],
        [
            "dagverðardalur",
            11,
            400,
            "Ísafjörður",
            "Vesturland og Vestfirðir",
            "Þéttbýli",
        ],
        ["Höfðabraut", 3, 801, "Selfoss", "Suðurland og Reykjanes", "Dreifbýli"],
    ]

    for p in POSTCODE_TO_PLACENAME:
        res = iceaddr_lookup(p[0], number=p[1], postcode=p[2])
        assert res[0]["stadur_nf"] == p[3]
        assert res[0]["svaedi"] == p[4]
        assert res[0]["tegund"] == p[5]

    assert len(iceaddr_lookup("Stærri-Árskógi", postcode=621)) > 0
    assert len(iceaddr_lookup("Grundarstíg")) > 10
    assert len(iceaddr_lookup("Grundarstíg", limit=2)) == 2


def test_address_suggestions():
    res = iceaddr_suggest("Öldugötu 4, 101")
    assert res[0]["heiti_nf"] == "Öldugata"
    assert res[0]["husnr"] == 4
    assert res[0]["stadur_nf"] == "Reykjavík"

    res = iceaddr_suggest("Öldugata 4, Rey")
    assert [n["stadur_tgf"] for n in res] == ["Reykjavík", "Reyðarfirði"]

    res = iceaddr_suggest("öldugötu 4b, 621")
    assert res[0]["bokst"] == "b"
    assert res[0]["stadur_tgf"] == "Dalvík"

    res = iceaddr_suggest("öldugötu 4B, 621")
    assert res and res[0]["bokst"] == "b"

    assert iceaddr_suggest("Öldugata a4B") == []
    assert iceaddr_suggest("Öldugötu 4Baaa") == []

    assert len(iceaddr_suggest("Kl")) == 0  # always empty for fewer than 3 chars
    assert len(iceaddr_suggest("Stærri B")) == 1
    assert len(iceaddr_suggest("öldu", limit=75)) == 75


def test_postcode_lookup():
    assert len(postcodes_for_placename("Kópavogur")) == 4
    assert len(postcodes_for_placename("kópavogi")) == 4
    assert len(postcodes_for_placename("kópav", partial=True)) == 4
    assert postcodes_for_placename("Selfossi") == [800, 801, 802]
    assert postcodes_for_placename("selfoss") == [800, 801, 802]
    assert postcodes_for_placename("SELFOS", partial=True) == [800, 801, 802]
