#!/usr/bin/env python3
"""

Create stadfong address database from from the
Staðfangaskrá CSV dataset.

From data compiled by Registers Iceland (CC-BY):
    https://opingogn.is/dataset/stadfangaskra
    https://opendefinition.org/licenses/cc-by/

"""

from typing import Any, Iterator

import csv
import os
import sqlite3
import sys
from builtins import input
from io import BytesIO, TextIOWrapper
from pathlib import Path
from urllib.request import urlopen

import humanize

from iceaddr.dist import in_iceland

STADFONG_REMOTE_URL = "https://fasteignaskra.is/Stadfangaskra.csv"

DSV_FILENAME = "Stadfangaskra.csv"

DEFAULT_DBNAME = "iceaddr.db"

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
]


def create_db(path: str) -> sqlite3.Connection:
    """Create stadfong database table."""
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
        long_wgs84 REAL
    );
    """

    dbconn.cursor().execute(create_table_sql)

    # Create indexes for common query patterns
    index_queries = [
        "CREATE INDEX idx_stadfong_heiti_nf ON stadfong(heiti_nf);",
        "CREATE INDEX idx_stadfong_heiti_tgf ON stadfong(heiti_tgf);",
        "CREATE INDEX idx_stadfong_postnr ON stadfong(postnr);",
        "CREATE INDEX idx_stadfong_heiti_husnr ON stadfong(heiti_nf, husnr);",
        "CREATE INDEX idx_stadfong_heiti_husnr_bokst ON stadfong(heiti_nf, husnr, bokst);",
        "CREATE INDEX idx_stadfong_serheiti ON stadfong(serheiti);",
        "CREATE INDEX idx_stadfong_coords ON stadfong(lat_wgs84, long_wgs84);",
    ]

    for query in index_queries:
        dbconn.cursor().execute(query)

    return dbconn


def read_rows(dsv_file: TextIOWrapper, delimiter: str = ",") -> Iterator[dict[Any, Any]]:
    reader = csv.DictReader(dsv_file, delimiter=delimiter)
    for row in reader:
        yield row


def insert_address_entry(e: dict[Any, Any], conn: sqlite3.Connection) -> None:
    # The stadfong datafile is quite dirty so we need to
    # sanitise values before inserting into the database

    for k in e:  # noqa: PLC0206
        e[k] = e[k].strip()

    # Icelandic to English decimal points
    e["LAT_WGS84"] = e["N_HNIT_WGS84"].replace(",", ".")
    e["LONG_WGS84"] = e["E_HNIT_WGS84"].replace(",", ".")

    to_int = ["BYGGD", "HEINUM", "HNITNUM", "HUSNR", "LANDNR", "POSTNR"]
    to_float = ["LAT_WGS84", "LONG_WGS84"]

    for k in to_int:
        if e[k] == "":
            e[k] = None
        else:
            try:
                e[k] = int(e[k])
            except Exception:
                print("Failed to convert '" + k + "' to int, setting to null")
                e[k] = None

    for k in to_float:
        if e[k] == "":
            e[k] = None
        else:
            try:
                e[k] = float(e[k])
            except Exception:
                print("Failed to convert '" + k + "' to float, setting to null")
                e[k] = None

    try:
        assert in_iceland((e["LAT_WGS84"], e["LONG_WGS84"]))
        qargs = [e[c.upper()] for c in COLS]
        # print(qargs)
        c = conn.cursor()
        c.execute("INSERT INTO stadfong VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", qargs)
    except Exception as exc:
        print(exc)


def main() -> None:
    # Optional args to specify input and output files
    stadfong_path = sys.argv[1] if len(sys.argv) > 1 else DSV_FILENAME
    db_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DBNAME

    if stadfong_path == DSV_FILENAME and not Path(stadfong_path).is_file():
        print("Fetching remote file %s" % STADFONG_REMOTE_URL)
        resp = urlopen(STADFONG_REMOTE_URL)
        f = TextIOWrapper(BytesIO(resp.read()), "utf-8")
    else:
        f = open(stadfong_path, "r")

    # Delete previous db file
    if Path(db_path).is_file():
        if input(f"{db_path} exists, overwrite? (y/n): ").lower().startswith("y"):
            Path(db_path).unlink()
        else:
            print("Aborting")
            sys.exit()

    # Create new database file
    dbconn = create_db(db_path)

    # Commit to DB in chunks of 1000 rows
    cnt = 0
    for r in read_rows(f):
        insert_address_entry(r, dbconn)
        cnt += 1
        if cnt % 1000 == 0:
            dbconn.commit()
            print("\tInserting: %d\r" % cnt, end="")
            sys.stdout.flush()

    dbconn.commit()

    print("\tInserting: %d\r" % cnt, end="")
    sys.stdout.flush()

    bytesize: int = os.stat(db_path).st_size
    human_size = humanize.naturalsize(bytesize)

    # After data import, analyze the database to optimize index usage
    dbconn.execute("ANALYZE;")

    print("\nCreated database with %d entries (%s)" % (cnt, human_size))


if __name__ == "__main__":
    """Command line invocation."""
    main()
