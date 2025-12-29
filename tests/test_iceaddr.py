"""

iceaddr: Look up information about Icelandic streets, addresses,
         placenames, landmarks, locations and postcodes.

Copyright (c) 2018-2025 Sveinbjorn Thordarson.

Tests for iceaddr python package.

"""

from typing import Optional

import datetime
import sys
from pathlib import Path

# Add parent directory to import path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from iceaddr import (
    POSTCODES,
    iceaddr_lookup,
    iceaddr_metadata,
    iceaddr_suggest,
    municipality_code_for_municipality,
    municipality_for_municipality_code,
    nearest_addr,
    nearest_addr_with_dist,
    nearest_placenames,
    nearest_placenames_with_dist,
    placename_lookup,
    postcode_lookup,
    postcodes_for_placename,
    postcodes_for_region,
    region_for_postcode,
)
from iceaddr.geo import ICELAND_COORDS, in_iceland, valid_wgs84_coord


def test_address_lookup():
    """Test address lookup using various known addresses."""
    ADDR_TO_POSTCODE = (  # noqa: N806
        ("Öldugata", 4, "Reykjavík", 101),
        ("öldugötu", 12, "hafnarfirði", 220),
        ("Tómasarhaga", 12, "Reykjavík", 107),
        ("smiðjuvegur", 22, "", 200),
    )

    for a in ADDR_TO_POSTCODE:
        res = iceaddr_lookup(a[0], number=a[1], placename=a[2])
        assert res[0]["postnr"] == a[3]

    res = iceaddr_lookup("Brattagata", number=4, letter="b")
    assert res[0]["postnr"] == 310
    assert res[0]["stadur_nf"] == "Borgarnes"

    POSTCODE_TO_PLACENAME = (  # noqa: N806
        ("Öldugata", 4, 101, "Reykjavík", "Höfuðborgarsvæðið", "Þéttbýli"),
        (
            "dagverðardalur",
            11,
            400,
            "Ísafjörður",
            "Vesturland og Vestfirðir",
            "Þéttbýli",
        ),
        ("Höfðabraut", 3, 805, "Selfoss", "Suðurland og Reykjanes", "Stærra dreifbýli"),
    )

    for p in POSTCODE_TO_PLACENAME:
        # print(f"iceaddr_lookup('{p[0]}', number={p[1]}, postcode={p[2]}"
        res = iceaddr_lookup(p[0], number=p[1], postcode=p[2])
        assert res[0]["stadur_nf"] == p[3]
        assert res[0]["svaedi_nf"] == p[4]
        # assert res[0]["tegund"] == p[5]

    assert len(iceaddr_lookup("Stærri-Árskógi", postcode=621)) > 0
    assert len(iceaddr_lookup("Grundarstíg")) > 10
    assert len(iceaddr_lookup("Grundarstíg", limit=2)) == 2


def test_address_lookup_matches_number_range_and_no_number():
    results = iceaddr_lookup("Vesturgata", number=6, placename="Reykjavík")
    assert results
    assert results[0]["vidsk"] == "6-8"
    assert results[0]["husnr"] is None


def test_address_lookup_can_find_places_of_interest():
    results = iceaddr_lookup("Hallgrímskirkja", postcode=101)
    assert len(results) == 1


def test_address_lookup_does_not_need_letter():
    assert iceaddr_lookup("Laugavegur", number=151)
    assert iceaddr_lookup("Laugavegur", number=151, letter="r")
    assert not iceaddr_lookup("Laugavegur", number=151, letter="e")


def test_address_suggestions():
    """Test address suggestions for natural language search strings."""
    res = iceaddr_suggest("Öldugötu 4, 101")
    assert res[0]["heiti_nf"] == "Öldugata"
    assert res[0]["husnr"] == 4
    assert res[0]["stadur_nf"] == "Reykjavík"
    assert res[0]["postnr"] == 101
    assert res[0]["svaedi_nf"] == "Höfuðborgarsvæðið"
    assert res[0]["svfheiti"] == "Reykjavíkurborg"

    res = iceaddr_suggest("Öldugata 4, Rey")
    assert [n["stadur_tgf"] for n in res] == ["Reykjavík", "Reyðarfirði"]

    res = iceaddr_suggest("öldugötu 4b, 621")
    assert res[0]["bokst"].lower() == "b"
    assert res[0]["stadur_tgf"] == "Dalvík"

    res = iceaddr_suggest("öldugötu 4B, 621")
    assert res
    assert res[0]["bokst"].lower() == "b"

    assert iceaddr_suggest("Öldugata a4B") == []
    assert iceaddr_suggest("Öldugötu 4Baaa") == []

    assert len(iceaddr_suggest("Kl")) == 0  # always empty for fewer than 3 chars
    assert len(iceaddr_suggest("öldu", limit=75)) == 75

    assert iceaddr_suggest("") == []
    assert iceaddr_suggest(" , , ") == []


def test_address_suggest_with_dashed_numbers():
    assert iceaddr_suggest("Laugavegur 151-155")


def test_postcode_data_integrity():
    """Make sure postcode data is sane."""
    for k, v in POSTCODES.items():
        assert type(k) is int
        _verify_postcode_dict(v)


def _verify_postcode_dict(pcd: Optional[dict[str, str]]):
    """Verify the integrity of a postcode dict."""
    assert pcd is not None
    assert "svaedi_nf" in pcd
    assert "svaedi_tgf" in pcd
    assert "stadur_nf" in pcd
    assert "stadur_tgf" in pcd
    assert "tegund" in pcd
    assert "lysing" not in pcd or pcd["lysing"] != ""


def test_postcode_lookup():
    """Test postcode lookup functions."""
    _verify_postcode_dict(postcode_lookup(101))
    _verify_postcode_dict(postcode_lookup(900))
    _record102 = postcode_lookup("102")
    _verify_postcode_dict(_record102)
    assert _record102
    assert _record102["stadur_nf"] == "Reykjavík"

    kop_pc_num = 5
    assert len(postcodes_for_placename("Kópavogur")) == kop_pc_num
    assert len(postcodes_for_placename("kópavogi")) == kop_pc_num
    assert len(postcodes_for_placename("kópav", partial=True)) == kop_pc_num

    selfoss_pc = [800, 801, 802, 803, 804, 805, 806]
    assert postcodes_for_placename("Selfossi") == selfoss_pc
    assert postcodes_for_placename("selfoss") == selfoss_pc
    assert postcodes_for_placename("SELFOS", partial=True) == selfoss_pc

    assert postcodes_for_region("Norðurland")
    assert postcodes_for_region("Austurland")
    assert postcodes_for_region("Höfuðborgarsvæðið")
    assert postcodes_for_region("Norður", partial=True)

    assert region_for_postcode(101) == "Höfuðborgarsvæðið"
    assert region_for_postcode(900) == "Suðurland og Reykjanes"
    assert region_for_postcode(710) == "Austurland"
    assert region_for_postcode(123459843) is None


def test_municipality_lookup():
    """Test municipality code lookup functions."""
    assert municipality_code_for_municipality("Reykjavíkurborg") == 0
    assert municipality_code_for_municipality("Blerghsmergh") is None

    assert municipality_for_municipality_code(0) == "Reykjavíkurborg"


def test_placename_lookup():
    """Test placename lookup."""
    assert len(placename_lookup("Meðalfellsvatn")) != 0
    assert len(placename_lookup("Meðalfell", partial=True)) != 0
    assert len(placename_lookup("Hellisheiði")) > 1


def test_in_iceland():
    """Test if coordinates are within Iceland."""
    assert in_iceland(ICELAND_COORDS)


def test_valid_wgs84_coord():
    """Test WGS84 coordinate validation."""
    # Valid coordinates
    assert valid_wgs84_coord(64.1560233, -21.951407)  # Reykjavik
    assert valid_wgs84_coord(0.0, 0.0)  # Null Island
    assert valid_wgs84_coord(45.0, 90.0)  # Valid coords

    # Edge cases - valid boundaries
    assert valid_wgs84_coord(90.0, 180.0)  # North Pole, date line
    assert valid_wgs84_coord(-90.0, -180.0)  # South Pole, date line
    assert valid_wgs84_coord(90.0, -180.0)
    assert valid_wgs84_coord(-90.0, 180.0)

    # Invalid latitude (out of range)
    assert not valid_wgs84_coord(90.1, 0.0)
    assert not valid_wgs84_coord(-90.1, 0.0)
    assert not valid_wgs84_coord(100.0, 0.0)
    assert not valid_wgs84_coord(-100.0, 0.0)

    # Invalid longitude (out of range)
    assert not valid_wgs84_coord(0.0, 180.1)
    assert not valid_wgs84_coord(0.0, -180.1)
    assert not valid_wgs84_coord(0.0, 200.0)
    assert not valid_wgs84_coord(0.0, -200.0)

    # Both invalid
    assert not valid_wgs84_coord(100.0, 200.0)
    assert not valid_wgs84_coord(-100.0, -200.0)


FISKISLOD_31_COORDS = (64.1560233, -21.951407)
OLDUGATA_4_COORDS = (64.148446, -21.944933)
POSTCODE_101 = 101


def test_nearest_addr():
    """Test address proxmity function."""
    addr = nearest_addr(FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1])
    assert len(addr) == 1
    assert addr[0]["heiti_nf"] == "Fiskislóð"
    assert addr[0]["postnr"] == POSTCODE_101
    assert addr[0]["svaedi_nf"] == "Höfuðborgarsvæðið"

    expected_num = 3
    addr = nearest_addr(OLDUGATA_4_COORDS[0], OLDUGATA_4_COORDS[1], limit=expected_num)
    assert len(addr) == expected_num
    assert addr[0]["heiti_nf"] == "Öldugata"
    assert addr[0]["postnr"] == POSTCODE_101
    assert addr[0]["svaedi_tgf"] == "Höfuðborgarsvæðinu"


def test_nearest_placename():
    """Test placename proximity function."""
    pn = nearest_placenames(FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1])
    assert len(pn) == 1
    assert pn[0]["nafn"] == "Grandi"

    pn = nearest_placenames(OLDUGATA_4_COORDS[0], OLDUGATA_4_COORDS[1], limit=5)
    assert len(pn) == 5
    assert "Landakotshæð" in [x["nafn"] for x in pn]


def test_nearest_max_dist():
    """Test max_dist parameter for nearest address and placename functions."""
    # First, test with a max_dist that is too small
    addr = nearest_addr(FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1], max_dist=0.001)
    assert addr == []
    pn = nearest_placenames(FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1], max_dist=0.001)
    assert pn == []

    # Then, test with a max_dist that is large enough
    addr = nearest_addr(FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1], max_dist=1.0)
    assert len(addr) == 1
    pn = nearest_placenames(FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1], max_dist=1.0)
    assert len(pn) == 1


def test_nearest_addr_with_dist():
    """Test nearest_addr_with_dist returns addresses with distances."""
    # Test single result
    results = nearest_addr_with_dist(FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1])
    assert len(results) == 1
    assert isinstance(results, list)
    assert isinstance(results[0], tuple)
    assert len(results[0]) == 2

    addr, dist = results[0]
    assert isinstance(addr, dict)
    assert isinstance(dist, float)
    assert addr["heiti_nf"] == "Fiskislóð"
    assert addr["postnr"] == POSTCODE_101
    assert dist > 0  # Distance should be positive
    assert dist < 1.0  # Should be less than 1km away

    # Test multiple results
    results = nearest_addr_with_dist(OLDUGATA_4_COORDS[0], OLDUGATA_4_COORDS[1], limit=5)
    assert len(results) == 5

    # Verify all results have correct format
    for addr, dist in results:
        assert isinstance(addr, dict)
        assert isinstance(dist, float)
        assert "heiti_nf" in addr
        assert "postnr" in addr
        assert dist > 0

    # Verify distances are sorted (ascending)
    distances = [dist for _, dist in results]
    assert distances == sorted(distances)

    # Verify first result matches
    assert results[0][0]["heiti_nf"] == "Öldugata"
    assert results[0][0]["postnr"] == POSTCODE_101

    # Test consistency with nearest_addr (without distances)
    addrs_without_dist = nearest_addr(OLDUGATA_4_COORDS[0], OLDUGATA_4_COORDS[1], limit=5)
    addrs_with_dist = nearest_addr_with_dist(OLDUGATA_4_COORDS[0], OLDUGATA_4_COORDS[1], limit=5)
    assert len(addrs_without_dist) == len(addrs_with_dist)
    for _, (addr_with, (addr_dict, _)) in enumerate(zip(addrs_without_dist, addrs_with_dist)):
        assert addr_with == addr_dict


def test_nearest_placenames_with_dist():
    """Test nearest_placenames_with_dist returns placenames with distances."""
    # Test single result
    results = nearest_placenames_with_dist(FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1])
    assert len(results) == 1
    assert isinstance(results, list)
    assert isinstance(results[0], tuple)
    assert len(results[0]) == 2

    place, dist = results[0]
    assert isinstance(place, dict)
    assert isinstance(dist, float)
    assert place["nafn"] == "Grandi"
    assert dist > 0  # Distance should be positive
    assert dist < 1.0  # Should be less than 1km away

    # Test multiple results
    results = nearest_placenames_with_dist(OLDUGATA_4_COORDS[0], OLDUGATA_4_COORDS[1], limit=5)
    assert len(results) == 5

    # Verify all results have correct format
    for place, dist in results:
        assert isinstance(place, dict)
        assert isinstance(dist, float)
        assert "nafn" in place
        assert dist > 0

    # Verify distances are sorted (ascending)
    distances = [dist for _, dist in results]
    assert distances == sorted(distances)

    # Verify expected placename is in results
    placenames = [place["nafn"] for place, _ in results]
    assert "Landakotshæð" in placenames

    # Test consistency with nearest_placenames (without distances)
    places_without_dist = nearest_placenames(OLDUGATA_4_COORDS[0], OLDUGATA_4_COORDS[1], limit=5)
    places_with_dist = nearest_placenames_with_dist(
        OLDUGATA_4_COORDS[0], OLDUGATA_4_COORDS[1], limit=5
    )
    assert len(places_without_dist) == len(places_with_dist)
    for _, (place_with, (place_dict, _)) in enumerate(zip(places_without_dist, places_with_dist)):
        assert place_with == place_dict


def test_nearest_with_dist_max_dist():
    """Test max_dist parameter works correctly with _with_dist functions."""
    # Test with max_dist that excludes all results
    addr_results = nearest_addr_with_dist(
        FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1], max_dist=0.001
    )
    assert addr_results == []

    place_results = nearest_placenames_with_dist(
        FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1], max_dist=0.001
    )
    assert place_results == []

    # Test with max_dist that includes results
    addr_results = nearest_addr_with_dist(
        FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1], limit=10, max_dist=0.5
    )
    # All returned results should be within max_dist
    for _, dist in addr_results:
        assert dist <= 0.5

    place_results = nearest_placenames_with_dist(
        FISKISLOD_31_COORDS[0], FISKISLOD_31_COORDS[1], limit=10, max_dist=1.0
    )
    # All returned results should be within max_dist
    for _, dist in place_results:
        assert dist <= 1.0


def test_metadata():
    """Test database metadata function."""
    metadata = iceaddr_metadata()

    assert isinstance(metadata, dict) and "date_created" in metadata
    date_created = metadata["date_created"]

    # Should be a datetime object with timezone info
    assert isinstance(date_created, datetime.datetime)
    assert date_created.tzinfo is not None

    # Should be a date that makes sense
    now = datetime.datetime.now(datetime.timezone.utc)
    assert date_created <= now
    project_start = datetime.datetime(2018, 1, 1, tzinfo=datetime.timezone.utc)
    assert date_created >= project_start
