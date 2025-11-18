"""Export project quantities to JSON."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.models import ProjectQuantities


class JSONExporter:
    def export(self, quantities: ProjectQuantities, output_path: Path) -> Path:
        payload = {
            "hvac": [q.__dict__ for q in quantities.hvac],
            "plumbing": quantities.plumbing.__dict__,
            "underfloor": quantities.underfloor.__dict__,
        }
        output_path.write_text(json.dumps(payload, indent=2))
        return output_path

