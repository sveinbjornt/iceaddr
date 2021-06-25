#!/usr/bin/env python3
"""

    Add placename data to iceaddr database.

"""

import fiona
import sqlite3
from pprint import pprint

# This file should be placed in repo root before running this program
GPKG_FILE = "ornefni.gpkg"

LAYERS = [
    "ornefni_flakar",
    "ornefni_linur",
    "ornefni_punktar",
]

DEFAULT_DBNAME = "iceaddr.db"


def center_point(coords):
    """ Find the center point of a given set of coordinates. """
    x = 0
    y = 0

    for px, py in coords:
        x += px
        y += py

    x = x / len(coords)
    y = y / len(coords)

    return (x, y)


def create_table(dbpath):
    """ Create ornefni database table. """
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


def delete_table(dbpath):
    """ Drop ornefni database table. """
    dbconn = sqlite3.connect(dbpath)

    del_table_sql = """DROP TABLE ornefni"""

    try:
        dbconn.cursor().execute(del_table_sql)
        print("Deleted pre-existing table 'ornefni'")
    except Exception:
        pass

    return dbconn


# Delete any existing table
delete_table(DEFAULT_DBNAME)

# Start by creating ornefni table
dbc = create_table(DEFAULT_DBNAME)
if not dbc:
    print("Failed to connect to DB")
    exit()

cursor = dbc.cursor()


# Read manual placename additions from text file, insert into ornefni DB table
print("Inserting placename additions")
f = open("placename_additions.txt", "r")
for line in f.readlines():
    if not line.strip() or line.strip().startswith("#"):
        continue
    comp = line.split(":")
    first = comp[0]
    last = comp[-1].strip()
    try:
        (lat, lon, fl) = last.split(",")
        lat = float(lat) if lat else None
        lon = float(lon) if lon else None
    except Exception:
        print(line)
        raise

    print("Inserting " + first)
    cursor.execute(
        "INSERT INTO ornefni (nafn, flokkur, lat_wgs84, long_wgs84) VALUES (?,?,?,?)",
        (first, fl, lat, lon),
    )

dbc.commit()


# Read IS50V geo layers from file, add all placenames ("örnefni") to DB
for layer in fiona.listlayers(GPKG_FILE):
    with fiona.open(GPKG_FILE, encoding="utf-8", layer=layer) as src:
        for i in src:

            wanted_layer = [layer.startswith(p) for p in LAYERS]
            if True not in wanted_layer:
                # print("Skipping layer " + layer)
                continue

            # pprint(i)
            try:
                fl = i["properties"]["ornefnaflokkur_text"]
                n = i["properties"]["nafnfitju"]
                c = i["geometry"]["coordinates"]
                nc = len(c)
            except Exception as e:
                print("ERROR adding item: {0}".format(e))
                print(n)
            else:
                print(n)

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
                    # print("Faulty flake: {0}".format(n))
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

            # Insert
            cursor.execute(
                "INSERT INTO ornefni (nafn, flokkur, lat_wgs84, long_wgs84) VALUES (?,?,?,?)",
                (n, fl, gps[0], gps[1]),
            )

        dbc.commit()
