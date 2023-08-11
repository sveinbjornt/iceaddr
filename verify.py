from typing import Tuple

ICELAND_COORDS = (64.9957538607, -18.5739616708)


def in_iceland(loc: Tuple, km_radius: float = 300.0) -> bool:
    """Check if coordinates are within or very close to Iceland."""
    return distance(loc, ICELAND_COORDS) <= km_radius
