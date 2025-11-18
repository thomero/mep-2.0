"""Minimal polygon implementation used when shapely is unavailable."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple


@dataclass
class SimplePoint:
    x: float
    y: float


class SimplePolygon:
    def __init__(self, points: Iterable[Tuple[float, float]]) -> None:
        pts = list(points)
        if len(pts) < 3:
            raise ValueError("Polygon requires at least 3 points")
        self._points = [SimplePoint(*pt) for pt in pts]

    @property
    def area(self) -> float:
        area = 0.0
        pts = self._points
        for i in range(len(pts)):
            j = (i + 1) % len(pts)
            area += pts[i].x * pts[j].y
            area -= pts[j].x * pts[i].y
        return abs(area) / 2.0

    @property
    def centroid(self) -> SimplePoint:
        signed_area = 0.0
        cx = 0.0
        cy = 0.0
        pts = self._points
        for i in range(len(pts)):
            j = (i + 1) % len(pts)
            factor = pts[i].x * pts[j].y - pts[j].x * pts[i].y
            signed_area += factor
            cx += (pts[i].x + pts[j].x) * factor
            cy += (pts[i].y + pts[j].y) * factor
        signed_area *= 0.5
        if signed_area == 0:
            return SimplePoint(0, 0)
        cx /= 6.0 * signed_area
        cy /= 6.0 * signed_area
        return SimplePoint(cx, cy)

