#!/usr/bin/env python3
"""

    Add placename data to iceaddr database.

"""

import fiona
import math
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


def isnet93_to_wgs84(xx, yy):
    """ Convert isnet93 coordinates to WGS84.
        From https://github.com/pallih/Scraperwiki-scrapers/blob/master/isnet93_wgs84.py
    """
    x = xx
    y = yy
    a = 6378137.0
    f = 1 / 298.257222101
    lat1 = 64.25
    lat2 = 65.75
    latc = 65.00
    lonc = 19.00
    eps = 0.00000000001

    def fx(p):
        return a * math.cos(p / rho) / math.sqrt(1 - math.pow(e * math.sin(p / rho), 2))

    def f1(p):
        return math.log((1 - p) / (1 + p))

    def f2(p):
        return f1(p) - e * f1(e * p)

    def f3(p):
        return pol1 * math.exp((f2(math.sin(p / rho)) - f2sin1) * sint / 2)

    rho = 45 / math.atan2(1.0, 1.0)
    e = math.sqrt(f * (2 - f))
    dum = f2(math.sin(lat1 / rho)) - f2(math.sin(lat2 / rho))
    sint = 2 * (math.log(fx(lat1)) - math.log(fx(lat2))) / dum
    f2sin1 = f2(math.sin(lat1 / rho))
    pol1 = fx(lat1) / sint
    polc = f3(latc) + 500000.0
    peq = (
        a
        * math.cos(latc / rho)
        / (sint * math.exp(sint * math.log((45 - latc / 2) / rho)))
    )
    pol = math.sqrt(math.pow(x - 500000, 2) + math.pow(polc - y, 2))
    lat = 90 - 2 * rho * math.atan(math.exp(math.log(pol / peq) / sint))
    lon = 0
    fact = rho * math.cos(lat / rho) / sint / pol
    fact = rho * math.cos(lat / rho) / sint / pol
    delta = 1.0
    while math.fabs(delta) > eps:
        delta = (f3(lat) - pol) * fact
        lat += delta
    lon = -(lonc + rho * math.atan((500000 - x) / (polc - y)) / sint)

    return {"lat": round(lat, 7), "lng": round(lon, 7)}


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
        print("Unable to create ornefni table")
        exit()

    return dbconn


def delete_table(dbpath):
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


# Read manual placename additions from text file, insert into DB
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

    # If so, update it
    # Else, insert it

    # Check if already exists in name and category and is single
    res = cursor.execute(
        "SELECT * FROM ornefni WHERE nafn=? AND flokkur=?", [first, fl]
    )
    # print(res)
    matches = [row for row in res]
    if len(matches) > 1:
        print("More than one match for " + first)
    elif len(matches) == 1:
        print("Updating " + first)
        theid = matches[0][0]
        q = "UPDATE ornefni SET nafn=?, flokkur=?, lat_wgs84=?, long_wgs84=? WHERE id=?"
        qargs = [first, fl, lat, lon, theid]
        cursor.execute(q, qargs)
    else:
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

                # pprint(c)
                if not c:
                    #print("Faulty flake: {0}".format(n))
                    #pprint(i)
                    #raise
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

            gps = (cp[0], cp[1])

            # Insert
            cursor.execute(
                "INSERT INTO ornefni (nafn, flokkur, lat_wgs84, long_wgs84) VALUES (?,?,?,?)",
                (n, fl, gps[0], gps[1]),
            )

        dbc.commit()
