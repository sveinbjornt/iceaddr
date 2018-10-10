# -*- encoding: utf-8 -*-
"""

    Create stadfong address SQLite3 database from from the
    DSV file at ftp://ftp.skra.is/skra/STADFANG.dsv.zip
    
    From data compiled by Registers Iceland, see:
        https://opingogn.is/dataset/stadfangaskra
    
    License: http://opendefinition.org/licenses/cc-by/

"""

from __future__ import print_function
import sys
import os
import sqlite3
import unicodecsv
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

STADFONG_REMOTE_URL = "ftp://ftp.skra.is/skra/STADFANG.dsv.zip"
DSV_FILENAME = "STADFANG.dsv"

cols = ["hnitnum", "svfnr", "byggd", "landnr", "postnr", 
        "heiti_nf", "heiti_tgf", "husnr", "bokst", "serheiti", 
        "vidsk", "lat_wgs84", "long_wgs84", "x_isn93", "y_isn93"]

def create_db(path):
    dbconn = sqlite3.connect(path)

    addresses_table_sql = """
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
    dbconn.cursor().execute(addresses_table_sql)
    
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
    e['LAT_WGS84'] = e['LAT_WGS84'].replace(',','.')
    e['LONG_WGS84'] = e['LONG_WGS84'].replace(',','.')
    e['X_ISN93'] = e['X_ISN93'].replace(',','.')
    e['Y_ISN93'] = e['Y_ISN93'].replace(',','.')

    to_int = ['BYGGD', 'HEINUM', 'HNITNUM', 'HUSNR', 'LANDNR', 'POSTNR']
    to_float = ['LAT_WGS84', 'LONG_WGS84', 'X_ISN93', 'Y_ISN93']
        
    for k in to_int:
        if e[k] == '':
            e[k] = None
        else:
            try:
                e[k] = int(e[k])
            except:
                print("Failed to convert '" + k + "' to int, setting to null")
                e[k] = None
            
    for k in to_float:
        if e[k] == '':
            e[k] = None
        else:
            try:
                e[k] = float(e[k])
            except:
                print("Failed to convert '" + k + "' to float, setting to null")
                e[k] = None
    
    try:
        l = [e[c.upper()] for c in cols]
        c = dbconn.cursor()
        c.execute('INSERT INTO stadfong VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', l)        
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # Optional args to specify input and output files
    stadfong_path = sys.argv[1] if len(sys.argv) > 1 else DSV_FILENAME
    db_path = sys.argv[2] if len(sys.argv) > 2 else 'stadfangaskra.db'
    
    if stadfong_path == DSV_FILENAME and not Path(stadfong_path).is_file():
        # Fetch remote file
        print("Fetching file at URL %s" % STADFONG_REMOTE_URL)
        resp = urlopen(STADFONG_REMOTE_URL)
        zipfile = ZipFile(BytesIO(resp.read()))
        f = zipfile.open("STADFANG.dsv")   
    else:
        f = open(stadfong_path, "rb")
    
    # Delete previous db file
    if Path(db_path).is_file():
        os.remove(db_path)
    
    dbconn = create_db(db_path)
    
    cnt = 0    
    for r in read_rows(f):            
        insert_address_entry(r)
        cnt += 1
        if cnt % 1000 == 0:
            dbconn.commit()
            print("\tInserting: %d\r" % cnt, end='')
            sys.stdout.flush()
    
    dbconn.commit()
    print("\nCreated stadfong database with %d entries" % cnt)
    
    