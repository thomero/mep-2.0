"""Area aggregation helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

from app.core.models import RoomGeometry


@dataclass
class AreaSummary:
    total_area: float
    useful_area: float
    restricted_area: float


class AreaCalculator:
    RESTRICTED_KEYWORDS = {"wardrobe", "shower", "wc", "kitchen", "cabinet"}

    def summarize(self, rooms: Iterable[RoomGeometry]) -> AreaSummary:
        total = 0.0
        restricted = 0.0
        for room in rooms:
            total += room.area_sqm
            label = (room.label or "").lower()
            if any(keyword in label for keyword in self.RESTRICTED_KEYWORDS):
                restricted += room.area_sqm
        useful = max(total - restricted, 0)
        return AreaSummary(total_area=total, useful_area=useful, restricted_area=restricted)

