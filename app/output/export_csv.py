"""Generate BOQ style CSV outputs."""
from __future__ import annotations

import csv
from pathlib import Path

from app.core.models import ProjectQuantities


class CSVExporter:
    def export(self, quantities: ProjectQuantities, output_path: Path) -> Path:
        with output_path.open("w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Section", "Description", "Quantity", "Unit"])
            for rec in quantities.hvac:
                writer.writerow(["HVAC", rec.room_id, f"{rec.required_btus:.0f}", rec.recommended_unit])
            writer.writerow(["Plumbing", "Hot water points", quantities.plumbing.hot_water_points, "points"])
            writer.writerow(["Plumbing", "Cold water points", quantities.plumbing.cold_water_points, "points"])
            writer.writerow(["Plumbing", "Sewage points", quantities.plumbing.sewage_points, "points"])
            writer.writerow(["Plumbing", "Floor drains", quantities.plumbing.floor_drains, "ea"])
            writer.writerow(["Plumbing", "Estimated pipe length", f"{quantities.plumbing.estimated_pipe_length_m:.1f}", "m"])
            writer.writerow([
                "Underfloor",
                "Total area",
                f"{quantities.underfloor.total_area_sqm:.2f}",
                "sqm",
            ])
            writer.writerow([
                "Underfloor",
                "Heated area",
                f"{quantities.underfloor.heated_area_sqm:.2f}",
                "sqm",
            ])
            writer.writerow([
                "Underfloor",
                "Restricted area",
                f"{quantities.underfloor.restricted_area_sqm:.2f}",
                "sqm",
            ])
            writer.writerow(["Underfloor", "Circuits", quantities.underfloor.circuits, "ea"])
            writer.writerow([
                "Underfloor",
                "Estimated pipe length",
                f"{quantities.underfloor.estimated_pipe_length_m:.1f}",
                "m",
            ])
        return output_path

