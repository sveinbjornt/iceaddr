"""

iceaddr: Look up information about Icelandic streets, addresses,
        placenames, landmarks, locations and postcodes.

Copyright (c) 2018-2025 Sveinbjorn Thordarson.

This file contains shared logic for nearest-neighbor spatial queries.

"""

from __future__ import annotations

from typing import Any, Callable

from .db import shared_db
from .geo import distance


def find_nearest(
    lat: float,
    lon: float,
    rtree_table: str,
    main_table: str,
    id_column: str,
    limit: int = 1,
    max_dist: float = 0.0,
    post_process: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
) -> list[tuple[dict[str, Any], float]]:
    """Generic nearest-neighbor search using R-Tree spatial indexing.

    Args:
        lat: Latitude in WGS84
        lon: Longitude in WGS84
        rtree_table: Name of the R-Tree virtual table (e.g., 'stadfong_rtree')
        main_table: Name of the main data table (e.g., 'stadfong')
        id_column: Name of the ID column in main table (e.g., 'hnitnum' or 'id')
        limit: Maximum number of results to return
        max_dist: Optional maximum distance in km (0.0 = no limit)
        post_process: Optional function to postprocess each result dict

    Returns:
        List of tuples of (dict, distance_km) for the nearest locations
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
            WHERE max_long >= ? AND min_long <= ? AND max_lat >= ? AND min_lat <= ?
        """
        # Standard R-Tree overlap check: box overlaps if it's not entirely outside
        params = [
            lon - search_radius,  # Not entirely west of search box
            lon + search_radius,  # Not entirely east of search box
            lat - search_radius,  # Not entirely south of search box
            lat + search_radius,  # Not entirely north of search box
        ]
        res = cur.execute(q_ids, params)
        ids = [r["id"] for r in res]

        if len(ids) >= min_candidates:
            break
        search_radius *= 2  # Double the search area

    if not ids:
        # Fallback for very sparse areas, using the old brute-force method.
        # This should be rare.
        res = list(db_conn.cursor().execute(f"SELECT * FROM {main_table}", []))
    else:
        # We have candidate IDs, now fetch their full details
        q_detail = f"SELECT * FROM {main_table} WHERE {id_column} IN ({','.join(['?'] * len(ids))})"
        res = list(db_conn.cursor().execute(q_detail, ids))

    # Compute distance once for each result and pair with the data
    # This avoids computing distance twice (once for sort, once for filter)
    with_distances = [(x, distance((lat, lon), (x["lat_wgs84"], x["long_wgs84"]))) for x in res]

    # Sort by distance
    closest = sorted(with_distances, key=lambda t: t[1])

    # Filter by max_dist before slicing if specified
    if max_dist > 0.0:
        closest = [(x, d) for x, d in closest if d <= max_dist]

    # Take top limit results, convert to dicts and apply post-processing
    results_with_dist: list[tuple[dict[str, Any], float]] = []
    for x, dist in closest[:limit]:
        result: dict[str, Any] = dict(x)
        if post_process:
            result = post_process(result)
        results_with_dist.append((result, dist))

    return results_with_dist
