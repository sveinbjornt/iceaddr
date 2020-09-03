"""

    test_iceaddr.py

    Tests for iceaddr package

"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../")

from iceaddr import (
    iceaddr_lookup,
    iceaddr_suggest,
    postcode_lookup,
    postcodes_for_placename,
    postcodes_for_region,
    POSTCODES,
    closest_addr,
    closest_placename,
)


def test_address_lookup():
    """ Test address lookup using various known addresses. """
    ADDR_TO_POSTCODE = [
        ["Öldugata", 4, "Reykjavík", 101],
        ["öldugötu", 12, "hafnarfirði", 220],
        ["Tómasarhaga", 12, "Reykjavík", 107],
        ["smiðjuvegur", 22, None, 200],
    ]

    for a in ADDR_TO_POSTCODE:
        res = iceaddr_lookup(a[0], number=a[1], placename=a[2])
        assert res and res[0]["postnr"] == a[3]

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
        ["Höfðabraut", 3, 805, "Selfoss", "Suðurland og Reykjanes", "Þéttbýli"],
    ]

    for p in POSTCODE_TO_PLACENAME:
        print("iceaddr_lookup('{0}', number={1}, postcode={2}".format(p[0], p[1], p[2]))
        res = iceaddr_lookup(p[0], number=p[1], postcode=p[2])
        assert res[0]["stadur_nf"] == p[3]
        assert res[0]["svaedi_nf"] == p[4]
        assert res[0]["tegund"] == p[5]

    assert len(iceaddr_lookup("Stærri-Árskógi", postcode=621)) > 0
    assert len(iceaddr_lookup("Grundarstíg")) > 10
    assert len(iceaddr_lookup("Grundarstíg", limit=2)) == 2


def test_address_lookup_does_not_need_letter():
    assert iceaddr_lookup("Laugavegur", number=151)
    assert iceaddr_lookup("Laugavegur", number=151, letter='r')
    assert not iceaddr_lookup("Laugavegur", number=151, letter='e')


def test_address_suggestions():
    """ Test address suggestions for natural language search strings. """
    res = iceaddr_suggest("Öldugötu 4, 101")
    assert res[0]["heiti_nf"] == "Öldugata"
    assert res[0]["husnr"] == 4
    assert res[0]["stadur_nf"] == "Reykjavík"

    res = iceaddr_suggest("Öldugata 4, Rey")
    assert [n["stadur_tgf"] for n in res] == ["Reykjavík", "Reyðarfirði"]

    res = iceaddr_suggest("öldugötu 4b, 621")
    assert res[0]["bokst"].lower() == "b"
    assert res[0]["stadur_tgf"] == "Dalvík"

    res = iceaddr_suggest("öldugötu 4B, 621")
    assert res and res[0]["bokst"].lower() == "b"

    assert iceaddr_suggest("Öldugata a4B") == []
    assert iceaddr_suggest("Öldugötu 4Baaa") == []

    assert len(iceaddr_suggest("Kl")) == 0  # always empty for fewer than 3 chars
    assert len(iceaddr_suggest("öldu", limit=75)) == 75


def test_address_suggest_with_dashed_numbers():
    assert iceaddr_suggest("Laugavegur 151-155")


def test_postcode_data_integrity():
    """ Make sure postcode data is OK. """
    for k, v in POSTCODES.items():
        assert type(k) == int
        _verify_postcode_dict(v)


def _verify_postcode_dict(pcd):
    """ Verify the integrity of a postcode dict. """
    assert "svaedi_nf" in pcd
    assert "svaedi_tgf" in pcd
    assert "stadur_nf" in pcd
    assert "stadur_tgf" in pcd
    assert "tegund" in pcd


def test_postcode_lookup():
    """ Test postcode lookup functions. """
    _verify_postcode_dict(postcode_lookup(101))
    _verify_postcode_dict(postcode_lookup(900))
    assert postcode_lookup("102")["stadur_nf"] == "Reykjavík"

    kop_pc_num = 5
    assert len(postcodes_for_placename("Kópavogur")) == kop_pc_num
    assert len(postcodes_for_placename("kópavogi")) == kop_pc_num
    assert len(postcodes_for_placename("kópav", partial=True)) == kop_pc_num

    selfoss_pc = [800, 801, 802, 803, 804, 805, 806]
    assert postcodes_for_placename("Selfossi") == selfoss_pc
    assert postcodes_for_placename("selfoss") == selfoss_pc
    assert postcodes_for_placename("SELFOS", partial=True) == selfoss_pc

    assert postcodes_for_region("Norðurland")
    assert postcodes_for_region("Höfuðborgarsvæðið")


FISKISLOD_31_COORDS = (64.1560233, -21.951407)
OLDUGATA_4_COORDS = (64.148446, -21.944933)


def test_closest_addr():
    """ Test address proxmity function. """
    addr = closest_addr(FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1])
    assert len(addr) == 1
    assert addr[0]["heiti_nf"] == "Fiskislóð"
    assert addr[0]["postnr"] == 101
    assert addr[0]["svaedi_nf"] == "Höfuðborgarsvæðið"

    addr = closest_addr(OLDUGATA_4_COORDS[0], OLDUGATA_4_COORDS[1], limit=3)
    assert len(addr) == 3
    assert addr[0]["heiti_nf"] == "Öldugata"
    assert addr[0]["postnr"] == 101
    assert addr[0]["svaedi_tgf"] == "Höfuðborgarsvæðinu"


def test_closest_placename():
    """ Test placename proximity function. """
    pn = closest_placename(FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1])
    assert len(pn) == 1
    assert pn[0]["nafn"] == "Grandi"

    pn = closest_placename(OLDUGATA_4_COORDS[0], OLDUGATA_4_COORDS[1], limit=5)
    assert len(pn) == 5
    assert "Landakotshæð" in [x["nafn"] for x in pn]
