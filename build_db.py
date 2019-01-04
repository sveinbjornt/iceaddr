# -*- encoding: utf-8 -*-
"""
    Create stadfong address database from from the
    DSV file at ftp://ftp.skra.is/skra/STADFANG.dsv.zip
    
    From data compiled by Registers Iceland (CC-BY):
        https://opingogn.is/dataset/stadfangaskra
        https://opendefinition.org/licenses/cc-by/
"""

from __future__ import print_function
from __future__ import unicode_literals

from builtins import input

import sys
import os
import sqlite3
import unicodecsv
import humanize
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


STADFONG_REMOTE_URL = "ftp://ftp.skra.is/skra/STADFANG.dsv.zip"
DSV_FILENAME = "STADFANG.dsv"
DEFAULT_DBNAME = "stadfangaskra.db"

COLS = [
    "hnitnum",
    "svfnr",
    "byggd",
    "landnr",
    "postnr",
    "heiti_nf",
    "heiti_tgf",
    "husnr",
    "bokst",
    "serheiti",
    "vidsk",
    "lat_wgs84",
    "long_wgs84",
    "x_isn93",
    "y_isn93",
]


def create_db(path):
    dbconn = sqlite3.connect(path)

    create_table_sql = """
    CREATE TABLE stadfong (
    hnitnum INTEGER UNIQUE PRIMARY KEY NOT NULL, 
    svfnr INTEGER,
    byggd INTEGER,
    landnr INTEGER,
    postnr INTEGER,
    heiti_nf TEXT,
    heiti_tgf TEXT,
    husnr INTEGER,
    bokst TEXT,
    serheiti TEXT,
    vidsk TEXT,
    lat_wgs84 REAL,
    long_wgs84 REAL,
    x_isn93 REAL,
    y_isn93 REAL
    );
    """

    dbconn.cursor().execute(create_table_sql)

    return dbconn


def read_rows(dsv_file, delimiter="|", encoding="utf8"):
    reader = unicodecsv.DictReader(dsv_file, delimiter=delimiter, encoding=encoding)
    for row in reader:
        yield row


def insert_address_entry(e):
    # The stadfong datafile is quite dirty so we need to
    # sanitise values before inserting into the database

    for k in e:
        e[k] = e[k].strip()

    # Icelandic to English decimal points
    e["LAT_WGS84"] = e["LAT_WGS84"].replace(",", ".")
    e["LONG_WGS84"] = e["LONG_WGS84"].replace(",", ".")
    e["X_ISN93"] = e["X_ISN93"].replace(",", ".")
    e["Y_ISN93"] = e["Y_ISN93"].replace(",", ".")

    to_int = ["BYGGD", "HEINUM", "HNITNUM", "HUSNR", "LANDNR", "POSTNR"]
    to_float = ["LAT_WGS84", "LONG_WGS84", "X_ISN93", "Y_ISN93"]

    for k in to_int:
        if e[k] == "":
            e[k] = None
        else:
            try:
                e[k] = int(e[k])
            except:
                print("Failed to convert '" + k + "' to int, setting to null")
                e[k] = None

    for k in to_float:
        if e[k] == "":
            e[k] = None
        else:
            try:
                e[k] = float(e[k])
            except:
                print("Failed to convert '" + k + "' to float, setting to null")
                e[k] = None

    try:
        qargs = [e[c.upper()] for c in COLS]
        c = dbconn.cursor()
        c.execute("INSERT INTO stadfong VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", qargs)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # Optional args to specify input and output files
    stadfong_path = sys.argv[1] if len(sys.argv) > 1 else DSV_FILENAME
    db_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DBNAME

    if stadfong_path == DSV_FILENAME and not Path(stadfong_path).is_file():
        print("Fetching remote file %s" % STADFONG_REMOTE_URL)
        resp = urlopen(STADFONG_REMOTE_URL)
        zipfile = ZipFile(BytesIO(resp.read()))
        f = zipfile.open(DSV_FILENAME)
    else:
        f = open(stadfong_path, "rb")

    # Delete previous db file
    if Path(db_path).is_file():
        if input("%s exists, overwrite? (y/n): " % db_path).lower().startswith("y"):
            os.remove(db_path)
        else:
            print("Aborting")
            sys.exit()

    dbconn = create_db(db_path)

    cnt = 0
    for r in read_rows(f):
        insert_address_entry(r)
        cnt += 1
        if cnt % 1000 == 0:
            dbconn.commit()
            print("\tInserting: %d\r" % cnt, end="")
            sys.stdout.flush()

    dbconn.commit()

    bytesize = os.stat(db_path).st_size
    human_size = humanize.naturalsize(bytesize)

    print("\nCreated database with %d entries (%s)" % (cnt, human_size))
