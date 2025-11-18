"""Lightweight heuristics to normalize room labels."""
from __future__ import annotations

from typing import Iterable

from app.core.models import RoomGeometry


class RoomClassifier:
    KEYWORD_TO_CLASS = {
        "bed": "bedroom",
        "wc": "bathroom",
        "bath": "bathroom",
        "kit": "kitchen",
        "corr": "corridor",
        "liv": "living",
        "store": "storage",
    }

    def normalize(self, rooms: Iterable[RoomGeometry]) -> Iterable[RoomGeometry]:
        for room in rooms:
            label = (room.label or "").lower()
            for keyword, canonical in self.KEYWORD_TO_CLASS.items():
                if keyword in label:
                    room.attributes["category"] = canonical
                    break
            else:
                room.attributes["category"] = "other"
        return rooms

