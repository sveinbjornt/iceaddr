"""

iceaddr: Look up information about Icelandic streets, addresses,
         placenames, landmarks, locations and postcodes.

This file contains code related to database metadata.

"""

from __future__ import annotations

import datetime
from typing import Any

from .db import SharedDB


def iceaddr_metadata() -> dict[str, Any]:
    """Return all database metadata as a dictionary."""
    db = SharedDB()
    c = db.connection().cursor()

    try:
        c.execute("SELECT key, value FROM metadata")
        rows = c.fetchall()

        metadata: dict[str, Any] = {}
        for row in rows:
            key = row["key"]
            value = row["value"]

            # Automatically convert date_* keys to datetime objects
            if key.startswith("date_"):
                try:
                    metadata[key] = datetime.datetime.fromisoformat(value)
                except (ValueError, TypeError):
                    # If parsing fails, keep as string
                    metadata[key] = value
            else:
                metadata[key] = value

        return metadata
    except Exception:
        return {}
