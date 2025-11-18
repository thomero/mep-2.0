"""High level orchestration for the MEP extraction pipeline."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

from app.core.area_calculator import AreaCalculator
from app.core.geometry_extractor import GeometryExtractor
from app.core.hvac_calculator import HVACCalculator
from app.core.models import ProjectQuantities
from app.core.pdf_loader import PDFLoader
from app.core.plumbing_calculator import PlumbingCalculator
from app.core.room_classifier import RoomClassifier
from app.core.symbol_detector import SymbolDetector
from app.core.underfloor_calculator import UnderfloorCalculator
from app.output.export_csv import CSVExporter
from app.output.export_json import JSONExporter
from app.output.report_generator import PDFReportGenerator

LOGGER = logging.getLogger(__name__)


class MEPExtractionPipeline:
    def __init__(self) -> None:
        self.pdf_loader = PDFLoader()
        self.geometry_extractor = GeometryExtractor()
        self.room_classifier = RoomClassifier()
        self.hvac_calculator = HVACCalculator()
        self.plumbing_calculator = PlumbingCalculator()
        self.underfloor_calculator = UnderfloorCalculator()
        self.symbol_detector = SymbolDetector()
        self.area_calculator = AreaCalculator()
        self.csv_exporter = CSVExporter()
        self.json_exporter = JSONExporter()
        self.pdf_report = PDFReportGenerator()

    def run(self, pdf_path: Path, export_dir: Path) -> Dict[str, Path]:
        LOGGER.info("Starting pipeline for %s", pdf_path)
        self.pdf_loader.load(pdf_path)
        vector_data = list(self.pdf_loader._iterate_pages(pdf_path))  # type: ignore
        rooms = self.geometry_extractor.from_vectors(vector_data)
        labels = [text for page in vector_data for text in getattr(page, "text_items", [])]
        rooms = self.geometry_extractor.assign_labels(rooms, labels)
        rooms = list(self.room_classifier.normalize(rooms))
        raster_pages = self.pdf_loader.rasterize(pdf_path)
        symbols = self.symbol_detector.detect(raster_pages)

        hvac = self.hvac_calculator.recommendations(rooms)
        plumbing = self.plumbing_calculator.summarize(rooms, symbols)
        underfloor = self.underfloor_calculator.summarize(rooms)
        project_quantities = ProjectQuantities(hvac=hvac, plumbing=plumbing, underfloor=underfloor)

        export_dir.mkdir(parents=True, exist_ok=True)
        json_path = export_dir / "output.json"
        csv_path = export_dir / "output.csv"
        pdf_summary_path = export_dir / "summary.pdf"

        self.json_exporter.export(project_quantities, json_path)
        self.csv_exporter.export(project_quantities, csv_path)
        self.pdf_report.generate(project_quantities, pdf_summary_path)

        return {"json": json_path, "csv": csv_path, "pdf": pdf_summary_path}

