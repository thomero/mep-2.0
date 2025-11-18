"""Plumbing quantities derived from symbols and room classification."""
from __future__ import annotations

from collections import Counter
from typing import Iterable

from app.core.models import PlumbingQuantities, RoomGeometry, SymbolDetection

SYMBOL_TO_POINT = {
    "wc": {"sewage": 1, "cold": 1, "hot": 0},
    "basin": {"sewage": 1, "cold": 1, "hot": 1},
    "shower": {"sewage": 1, "cold": 1, "hot": 1},
    "bath": {"sewage": 1, "cold": 1, "hot": 1},
    "kitchen sink": {"sewage": 1, "cold": 1, "hot": 1},
    "washing machine": {"sewage": 1, "cold": 1, "hot": 1},
    "floor drain": {"floor_drain": 1},
}

PIPE_LENGTH_PER_POINT = 4.0  # meters average run


class PlumbingCalculator:
    def summarize(self, rooms: Iterable[RoomGeometry], symbols: Iterable[SymbolDetection]) -> PlumbingQuantities:
        counters = Counter()
        floor_drains = 0
        for symbol in symbols:
            rule = SYMBOL_TO_POINT.get(symbol.label.lower())
            if not rule:
                continue
            for key, value in rule.items():
                if key == "floor_drain":
                    floor_drains += value
                else:
                    counters[key] += value
        total_points = counters["hot"] + counters["cold"] + counters["sewage"]
        estimated_length = total_points * PIPE_LENGTH_PER_POINT
        return PlumbingQuantities(
            hot_water_points=counters["hot"],
            cold_water_points=counters["cold"],
            sewage_points=counters["sewage"],
            floor_drains=floor_drains,
            estimated_pipe_length_m=estimated_length,
        )

