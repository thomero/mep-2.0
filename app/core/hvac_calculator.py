"""HVAC load calculations based on room attributes."""
from __future__ import annotations

from typing import Iterable, List

from app.core.models import HVACRecommendation, RoomGeometry

CLIMATE_FACTOR = 35  # Cyprus typical BTU/m2
ROOM_TYPE_FACTORS = {
    "living": 1.2,
    "bedroom": 1.0,
    "kitchen": 1.1,
    "bathroom": 0.6,
    "corridor": 0.5,
    "storage": 0.4,
    "other": 0.8,
}


class HVACCalculator:
    def recommendations(self, rooms: Iterable[RoomGeometry]) -> List[HVACRecommendation]:
        output: List[HVACRecommendation] = []
        for room in rooms:
            category = room.attributes.get("category", "other")
            factor = ROOM_TYPE_FACTORS.get(category, ROOM_TYPE_FACTORS["other"])
            btus = room.area_sqm * CLIMATE_FACTOR * factor
            unit = self._select_unit(btus)
            output.append(HVACRecommendation(room.room_id, btus, unit))
        return output

    @staticmethod
    def _select_unit(btus: float) -> str:
        if btus < 9000:
            return "9k BTU"
        if btus < 12000:
            return "12k BTU"
        if btus < 18000:
            return "18k BTU"
        if btus < 24000:
            return "24k BTU"
        return "Multi-split"

