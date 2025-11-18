"""Geometry extraction from PDF vector data using shapely."""
from __future__ import annotations

import logging
from typing import Iterable, List, Optional

try:  # pragma: no cover
    from shapely.geometry import Polygon
except Exception:  # pragma: no cover
    from app.utils.simple_polygon import SimplePolygon as Polygon  # type: ignore

from app.core.models import RoomGeometry

LOGGER = logging.getLogger(__name__)


class GeometryExtractor:
    """Converts PDF vector shapes into usable polygons."""

    def __init__(self, min_room_area: float = 1.0) -> None:
        self.min_room_area = min_room_area

    def from_vectors(self, vector_pages: Iterable[dict]) -> List[RoomGeometry]:
        rooms: List[RoomGeometry] = []
        if Polygon is None:
            LOGGER.warning("Shapely not installed; returning empty room set")
            return rooms

        for page in vector_pages:
            page_number = _get(page, "page_number", 0)
            shapes = _get(page, "shapes", {}) or {}
            rects = shapes.get("rects", [])
            for idx, shape in enumerate(rects):
                polygon = Polygon([
                    (shape["x0"], shape["top"]),
                    (shape["x1"], shape["top"]),
                    (shape["x1"], shape["bottom"]),
                    (shape["x0"], shape["bottom"]),
                ])
                area_sqm = polygon.area / 10000.0
                if area_sqm < self.min_room_area:
                    continue
                room_id = f"p{page_number}_rect{idx}"
                rooms.append(RoomGeometry(room_id=room_id, polygon=polygon, area_sqm=area_sqm))
        LOGGER.info("Extracted %s rooms from vector data", len(rooms))
        return rooms

    def assign_labels(self, rooms: List[RoomGeometry], labels: Iterable[dict]) -> List[RoomGeometry]:
        label_lookup = {item.get("text", ""): item for item in labels}
        for room in rooms:
            matched_label: Optional[str] = None
            for text, data in label_lookup.items():
                bbox = data.get("x0"), data.get("top"), data.get("x1"), data.get("bottom")
                centroid = room.polygon.centroid
                if bbox[0] <= centroid.x <= bbox[2] and bbox[1] <= centroid.y <= bbox[3]:
                    matched_label = text
                    break
            if matched_label:
                room.label = matched_label
        return rooms


def _get(obj, key: str, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


