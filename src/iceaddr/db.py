"""

iceaddr: Look up information about Icelandic streets, addresses,
         placenames, landmarks, locations and postcodes.

Copyright (c) 2018-2025 Sveinbjorn Thordarson.

This file contains code related to the iceaddr sqlite3 database.

"""

import sqlite3
from importlib import resources

_DB_REL_PATH = "iceaddr.db"


class SharedDB:
    """Singleton object wrapper for local SQLite3 database."""

    def __init__(self):
        self.db_conn = None

    def connection(self) -> sqlite3.Connection:
        # Open connection lazily
        if not self.db_conn:
            db_path = resources.files("iceaddr").joinpath(_DB_REL_PATH)

            # Open database file in read-only mode via URI
            # As long as we're read-only, thread safety is not an issue
            db_uri = f"file:{db_path}?mode=ro"
            self.db_conn = sqlite3.connect(db_uri, uri=True, check_same_thread=False)

            # Return rows as key-value dicts
            self.db_conn.row_factory = lambda c, r: dict(  # type: ignore noqa: PGH003
                zip([col[0] for col in c.description], r)  # type: ignore noqa: PGH003
            )

        return self.db_conn


shared_db = SharedDB()
