"""Helpers for converting vector entities to shapely primitives."""
from __future__ import annotations

from typing import Iterable, List, Tuple

try:  # pragma: no cover
    from shapely.geometry import Polygon
except Exception:  # pragma: no cover
    Polygon = None  # type: ignore


def rect_to_polygon(rect: dict) -> "Polygon":  # pragma: no cover - simple wrapper
    if Polygon is None:
        raise RuntimeError("shapely is not installed")
    return Polygon(
        [
            (rect["x0"], rect["top"]),
            (rect["x1"], rect["top"]),
            (rect["x1"], rect["bottom"]),
            (rect["x0"], rect["bottom"]),
        ]
    )

