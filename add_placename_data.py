#!/usr/bin/env python3
"""

    Add placename data to iceaddr database.

    Fetches placename data from the IS50V geospatial database and inserts it
    into the iceaddr database. Also adds manual placename additions from
    placename_additions.txt.

"""

from typing import List, Tuple

from pprint import pprint  # type: ignore
import sqlite3
from pathlib import Path
from io import BytesIO
import zipfile

import fiona  # type: ignore
import requests

from iceaddr.dist import in_iceland


ORNEFNI_DATA_FILE = "is_50v_ornefni_wgs_84.gpkg"
ORNEFNI_DATA_URL = (
    "https://atlas.lmi.is/heikir/downloadData/is_50v_ornefni_wgs_84_gpkg.zip"
)

# Remote URL for latest IS50V data:
# https://atlas.lmi.is/heikir/downloadData/is_50v_ornefni_wgs_84_gpkg.zip
# This file should be placed in repo root and renamed before running this program
GPKG_FILE = "ornefni.gpkg"

LAYERS = [
    "ornefni_flakar",
    "ornefni_linur",
    "ornefni_punktar",
]


DEFAULT_DBNAME = "iceaddr.db"


def fetch_ornefni_data() -> None:
    """Fetch IS50V placename data from remote URL, unzip
    from memory to current directory and rename file."""

    r = requests.get(ORNEFNI_DATA_URL, allow_redirects=True)
    if r.status_code != 200:
        print(f"Failed to download {ORNEFNI_DATA_URL}")
        exit(1)

    z = zipfile.ZipFile(BytesIO(r.content))
    z.extractall()

    Path(ORNEFNI_DATA_FILE).rename(GPKG_FILE)


def center_point(coords: List[Tuple[float, float]]) -> Tuple[float, float]:
    """Find the center point of a given set of coordinates."""
    x: float = 0
    y: float = 0

    for px, py in coords:
        x += px
        y += py

    x = x / len(coords)
    y = y / len(coords)

    return (x, y)


def create_table(dbpath: str) -> sqlite3.Connection:
    """Create ornefni database table."""
    dbconn = sqlite3.connect(dbpath)

    create_table_sql = """
    CREATE TABLE ornefni (
        id INTEGER UNIQUE PRIMARY KEY NOT NULL,
        nafn TEXT,
        flokkur TEXT,
        lat_wgs84 REAL,
        long_wgs84 REAL
    );
    """

    try:
        dbconn.cursor().execute(create_table_sql)
    except Exception:
        print("Unable to create table 'ornefni'")
        exit()

    return dbconn


def delete_table(dbpath: str) -> sqlite3.Connection:
    """Drop ornefni database table."""
    dbconn = sqlite3.connect(dbpath)

    del_table_sql = """DROP TABLE ornefni"""

    try:
        dbconn.cursor().execute(del_table_sql)
        print("Deleted pre-existing table 'ornefni'")
    except Exception:
        pass

    return dbconn


def add_placename_additions(dbc: sqlite3.Connection) -> None:
    """Read manual placename additions from text file, insert into "ornefni" DB table."""
    print("Inserting placename additions")
    f = open("placename_additions.txt", "r")
    for line in f.readlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        comp = line.split(":")
        first = comp[0]
        last = comp[-1].strip()
        try:
            (latstr, lonstr, fl) = last.split(",")
            lat = float(latstr) if latstr else None
            lon = float(lonstr) if lonstr else None
        except Exception as e:
            print(f"{line}: error: {e}")
            raise

        # print("Inserting " + first)

        if lat and lon and not in_iceland((lat, lon)):
            raise Exception(f"Not in Iceland: {first} ({lat}, {lon})")

        dbc.cursor().execute(
            "INSERT INTO ornefni (nafn, flokkur, lat_wgs84, long_wgs84) VALUES (?,?,?,?)",
            (first, fl, lat, lon),
        )
    f.close()
    dbc.commit()


def add_placenames_from_is50v(dbc: sqlite3.Connection) -> None:
    """Read IS50V geo layers from file, add all placenames ("örnefni") to DB."""
    if not Path(GPKG_FILE).exists():
        print(f"Could not find file {GPKG_FILE}")
        exit(1)

    for layer in fiona.listlayers(GPKG_FILE):
        with fiona.open(GPKG_FILE, encoding="utf-8", layer=layer) as src:
            for i in src:
                wanted_layer = [layer.startswith(p) for p in LAYERS]
                if True not in wanted_layer:
                    # print("Skipping layer " + layer)
                    continue

                # pprint(i)
                try:
                    # pprint(i["properties"])
                    fl = i["properties"]["ornefnaflokkur"]
                    n = i["properties"]["ornefni"]
                    c = i["geometry"]["coordinates"]
                    # nc = len(c)
                except Exception as e:
                    print(f"ERROR adding item {i['properties']}: {e}")
                else:
                    pass
                    # print(n)

                # Special handling of lines (e.g. rivers)
                if layer.startswith("ornefni_linur"):
                    firstcoords = c[0]

                    if type(firstcoords[0]) is list:
                        firstcoords = firstcoords[0]

                    if type(firstcoords) is list:
                        firstcoords = firstcoords[0]
                    cp = firstcoords

                # Special handling of flakes - use center point
                elif type(c) is list:
                    if not c:
                        # print(f"Faulty flake: {n}")
                        # pprint(i)
                        # raise
                        continue

                    firstcoords = c[0]
                    t = type(firstcoords[0])
                    if t is float:
                        cp = firstcoords
                    elif t is list:
                        firstcoords = firstcoords[0]
                        cp = center_point(firstcoords)

                # Just a point
                else:
                    cp = c

                # LMÍ's GPKG coord values are reversed! Why?
                gps = (cp[1], cp[0])

                if not in_iceland(gps):
                    print(f"WARNING: Not in Iceland, skipping: {n} ({gps})")

                # Insert
                dbc.cursor().execute(
                    "INSERT INTO ornefni (nafn, flokkur, lat_wgs84, long_wgs84) VALUES (?,?,?,?)",
                    (n, fl, gps[0], gps[1]),
                )

            dbc.commit()


def main() -> None:
    # Fetch placename data from remote URL
    fetch_ornefni_data()

    # Delete any existing table
    delete_table(DEFAULT_DBNAME)

    # Start by creating ornefni table
    dbc = create_table(DEFAULT_DBNAME)
    if not dbc:
        print("Failed to connect to DB")
        exit(1)

    add_placename_additions(dbc)
    add_placenames_from_is50v(dbc)


if __name__ == "__main__":
    """Command line invocation."""
    main()
