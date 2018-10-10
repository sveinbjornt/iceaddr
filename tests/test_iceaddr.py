# -*- encoding: utf-8 -*-
"""

    test_iceaddr.py

    Tests for iceaddr package
    
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src/")

from iceaddr import iceaddr_lookup, postcodes_for_placename

def test_address_lookup():
    ADDR_TO_POSTCODE = [
        ['Öldugata', 4, 'Reykjavík', 101],
        ['Öldugötu', 12, 'Hafnarfirði', 220],
        ['Tómasarhaga', 12, 'Reykjavík', 107],
        ['Smiðjuvegur', 22, None, 200]
    ]
    
    for a in ADDR_TO_POSTCODE:
        res = iceaddr_lookup(a[0], number=a[1], placename=a[2])
        assert res[0]['postnr'] == a[3]
    
    res = iceaddr_lookup('Brattagata', number=4, letter='b')
    assert len(res) and res[0]['postnr'] == 310 and res[0]['stadur_nf'] == 'Borgarnes'
    
    POSTCODE_TO_PLACENAME = [
        ['Öldugata', 4, 101, 'Reykjavík', 'Höfuðborgarsvæðið', 'Þéttbýli'],
        ['Dagverðardalur', 11, 400, 'Ísafjörður', 'Vesturland og Vestfirðir', 'Þéttbýli'],
        ['Höfðabraut', 3, 801, 'Selfoss', 'Suðurland og Reykjanes', 'Dreifbýli']
    ]
    
    for p in POSTCODE_TO_PLACENAME:
        res = iceaddr_lookup(p[0], number=p[1], postcode=p[2])
        assert res[0]['stadur_nf'] == p[3]
        assert res[0]['svaedi'] == p[4]
        assert res[0]['tegund'] == p[5]
    
    assert len(iceaddr_lookup('Grundarstíg')) > 10
    
def test_postcode_lookup():
    assert len(postcodes_for_placename('Kópavogur')) == 4
    assert len(postcodes_for_placename('Kópavogi')) == 4
    assert postcodes_for_placename('Selfossi') == [800, 801, 802]
    
