"""

iceaddr: Look up information about Icelandic streets, addresses,
         placenames, landmarks, locations and postcodes.

This file contains code related to distance calculation.

"""

from typing import Optional

import math

EARTH_RADIUS_KM = 6371.0088

# A WGS84 (latitude, longitude) pair. Either component may be None, since some
# rows in the placename data carry no coordinates.
CoordType = tuple[Optional[float], Optional[float]]


def distance(loc1: CoordType, loc2: CoordType) -> float:
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
    https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    """
    (lat1, lon1) = loc1
    (lat2, lon2) = loc2

    # Missing coordinates, return infinity so they sort last. Note that this must
    # be an explicit None check: 0.0 is a perfectly valid latitude or longitude.
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return float("inf")

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    slat = math.sin(dlat / 2)
    slon = math.sin(dlon / 2)
    a = slat * slat + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * slon * slon
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c


ICELAND_COORDS = (64.9957538607, -18.5739616708)


def in_iceland(loc: tuple[float, float], km_radius: float = 800.0) -> bool:
    """Check if coordinates are within or very close to Iceland."""
    return distance(loc, ICELAND_COORDS) <= km_radius


def valid_wgs84_coord(lat: float, lon: float) -> bool:
    """Check if coordinates are valid WGS84 latitude and longitude coordinates."""
    if lat < -90.0 or lat > 90.0:
        return False
    if lon < -180.0 or lon > 180.0:
        return False
    return True
