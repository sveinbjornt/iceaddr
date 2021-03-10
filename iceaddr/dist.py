"""

    iceaddr: Look up information about Icelandic streets, addresses,
             placenames, landmarks, locations and postcodes.

    This file contains code related to distance calculation.

"""

from typing import Tuple

import math


_EARTH_RADIUS = 6371.0088  # Earth's radius in km


def distance(loc1: Tuple[float, float], loc2: Tuple[float, float]) -> float:
    """
    Calculate the Haversine distance.
    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)
    Returns
    -------
    distance_in_km : float
    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    Source:
    https://stackoverflow.com/questions/19412462
        /getting-distance-between-two-points-based-on-latitude-longitude
    """
    (lat1, lon1) = loc1
    (lat2, lon2) = loc2

    # Bad params, or missing coordinates, return infinity for distance-sorting purposes
    if not lat1 or not lon1 or not lat2 or not lon2:
        return float("inf")

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    slat = math.sin(dlat / 2)
    slon = math.sin(dlon / 2)
    a = (
        slat * slat
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * slon * slon
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return _EARTH_RADIUS * c
