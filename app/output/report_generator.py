"""Generate printable PDF summary reports."""
from __future__ import annotations

from pathlib import Path

from app.core.models import ProjectQuantities

try:  # pragma: no cover
    from fpdf import FPDF
except Exception:  # pragma: no cover
    FPDF = None  # type: ignore


class PDFReportGenerator:
    def generate(self, quantities: ProjectQuantities, output_path: Path) -> Path:
        if FPDF is None:
            # Fallback: write markdown-like text even if extension is pdf
            output_path.write_text(self._text_summary(quantities))
            return output_path
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="MEP Quantities Summary", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font_size(10)
        pdf.multi_cell(0, 8, txt=self._text_summary(quantities))
        pdf.output(str(output_path))
        return output_path

    def _text_summary(self, quantities: ProjectQuantities) -> str:
        lines = ["HVAC Recommendations:"]
        for rec in quantities.hvac:
            lines.append(f" - {rec.room_id}: {rec.required_btus:.0f} BTU ({rec.recommended_unit})")
        lines.append("\nPlumbing:")
        plumbing = quantities.plumbing
        lines.append(
            f" Hot: {plumbing.hot_water_points}, Cold: {plumbing.cold_water_points}, Sewage: {plumbing.sewage_points}"
        )
        lines.append(f" Floor drains: {plumbing.floor_drains}, Pipe length: {plumbing.estimated_pipe_length_m:.1f} m")
        u = quantities.underfloor
        lines.append("\nUnderfloor heating:")
        lines.append(
            f" Total {u.total_area_sqm:.2f} sqm, Heated {u.heated_area_sqm:.2f} sqm, Restricted {u.restricted_area_sqm:.2f} sqm"
        )
        lines.append(f" Coverage {u.coverage_ratio:.0%}, Circuits {u.circuits}, Pipe {u.estimated_pipe_length_m:.1f} m")
        return "\n".join(lines)

