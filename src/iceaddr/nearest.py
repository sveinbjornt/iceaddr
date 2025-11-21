"""

iceaddr: Look up information about Icelandic streets, addresses,
        placenames, landmarks, locations and postcodes.

Copyright (c) 2018-2025 Sveinbjorn Thordarson.

This file contains shared logic for nearest-neighbor spatial queries.

"""

from __future__ import annotations

from typing import Any, Callable

from .db import shared_db
from .dist import distance


def find_nearest(
    lat: float,
    lon: float,
    rtree_table: str,
    main_table: str,
    id_column: str,
    limit: int = 1,
    max_dist: float = 0.0,
    post_process: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """
    Generic nearest-neighbor search using R-Tree spatial indexing.

    Args:
        lat: Latitude in WGS84
        lon: Longitude in WGS84
        rtree_table: Name of the R-Tree virtual table (e.g., 'stadfong_rtree')
        main_table: Name of the main data table (e.g., 'stadfong')
        id_column: Name of the ID column in main table (e.g., 'hnitnum' or 'id')
        limit: Maximum number of results to return
        max_dist: Optional maximum distance in km (0.0 = no limit)
        post_process: Optional function to process each result dict

    Returns:
        List of dictionaries containing the nearest locations
    """
    db_conn = shared_db.connection()
    cur = db_conn.cursor()

    # Search within an expanding bounding box to find candidates
    search_radius = 0.01  # Start with a box of roughly 1.1km side
    ids = []
    # We want at least 'limit' candidates, but also a few more to sort through
    min_candidates = max(limit, 20)

    for _ in range(6):  # Expand search radius up to 6 times
        q_ids = f"""
            SELECT id FROM {rtree_table}
            WHERE min_long >= ? AND max_long <= ? AND min_lat >= ? AND max_lat <= ?
        """
        # We use native SQLite parameter substitution to avoid SQL injection
        params = [
            lon - search_radius,
            lon + search_radius,
            lat - search_radius,
            lat + search_radius,
        ]
        res = cur.execute(q_ids, params)
        ids = [r["id"] for r in res]

        if len(ids) >= min_candidates:
            break
        search_radius *= 2  # Double the search area

    if not ids:
        # Fallback for very sparse areas, using the old brute-force method.
        # This should be rare.
        res = db_conn.cursor().execute(f"SELECT * FROM {main_table}", [])
    else:
        # We have candidate IDs, now fetch their full details
        q_detail = f"SELECT * FROM {main_table} WHERE {id_column} IN ({','.join(['?'] * len(ids))})"
        res = list(db_conn.cursor().execute(q_detail, ids))

    # Sort the results by precise distance
    # The result from the DB is an iterator of sqlite3.Row objects
    closest = sorted(
        res,
        key=lambda i: distance((lat, lon), (i["lat_wgs84"], i["long_wgs84"])),
    )

    # Convert to dicts and apply post-processing if provided
    results: list[dict[str, Any]] = []
    for x in closest[:limit]:
        result: dict[str, Any] = dict(x)
        if post_process:
            result = post_process(result)
        results.append(result)

    # Optional max distance filter - filter all results within max_dist
    if max_dist > 0.0:
        filtered: list[dict[str, Any]] = [
            r
            for r in results
            if distance((lat, lon), (r["lat_wgs84"], r["long_wgs84"])) <= max_dist
        ]
        results = filtered

    return results
