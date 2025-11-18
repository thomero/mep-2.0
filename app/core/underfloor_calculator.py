"""Underfloor heating estimation routines."""
from __future__ import annotations

from math import ceil
from typing import Iterable

from app.core.area_calculator import AreaCalculator
from app.core.models import RoomGeometry, UnderfloorHeatingQuantities

PIPE_DENSITY_PER_SQM = 6.0  # meters of pipe per sqm
MAX_AREA_PER_CIRCUIT = 20.0


class UnderfloorCalculator:
    def __init__(self) -> None:
        self.area_calculator = AreaCalculator()

    def summarize(self, rooms: Iterable[RoomGeometry]) -> UnderfloorHeatingQuantities:
        summary = self.area_calculator.summarize(rooms)
        heated = summary.useful_area
        restricted = summary.restricted_area
        total = summary.total_area
        coverage = 0 if total == 0 else heated / total
        pipe_length = heated * PIPE_DENSITY_PER_SQM
        circuits = max(1, ceil(heated / MAX_AREA_PER_CIRCUIT)) if heated else 0
        return UnderfloorHeatingQuantities(
            total_area_sqm=total,
            heated_area_sqm=heated,
            restricted_area_sqm=restricted,
            coverage_ratio=coverage,
            circuits=circuits,
            estimated_pipe_length_m=pipe_length,
        )

