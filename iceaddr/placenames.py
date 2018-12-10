# -*- encoding: utf-8 -*-
"""
    iceaddr: Look up information about Icelandic street addresses and postcodes
    Copyright (c) 2018 Sveinbjorn Thordarson
"""

from __future__ import unicode_literals
from __future__ import print_function

import re
from .db import shared_db

def placename_lookup(placename):
    q = "SELECT * FROM ornefni WHERE nafn=?"

    db_conn = shared_db.connection()
    res = db_conn.cursor().execute(q, [placename])
    return [dict(row) for row in res]