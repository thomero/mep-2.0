"""Domain data models for MEP extraction pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class PageImage:
    """Represents a rasterized PDF page ready for CV tasks."""

    page_number: int
    image_path: Path
    width: int
    height: int
    dpi: int = 300


@dataclass
class RoomGeometry:
    """Polygon geometry and semantic info for a room."""

    room_id: str
    polygon: "Polygon"
    area_sqm: float
    label: Optional[str] = None
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class SymbolDetection:
    """Represents a detected mechanical/electrical/plumbing symbol."""

    label: str
    confidence: float
    bbox: Tuple[float, float, float, float]  # xmin, ymin, xmax, ymax
    page_number: int


@dataclass
class ExtractionResult:
    """Aggregates everything extracted from a PDF plan."""

    file_path: Path
    rooms: List[RoomGeometry] = field(default_factory=list)
    symbols: List[SymbolDetection] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class HVACRecommendation:
    """HVAC requirements per room."""

    room_id: str
    required_btus: float
    recommended_unit: str


@dataclass
class PlumbingQuantities:
    """Aggregated plumbing requirements for a plan."""

    hot_water_points: int
    cold_water_points: int
    sewage_points: int
    floor_drains: int
    estimated_pipe_length_m: float


@dataclass
class UnderfloorHeatingQuantities:
    """Coverage estimations for underfloor heating designs."""

    total_area_sqm: float
    heated_area_sqm: float
    restricted_area_sqm: float
    coverage_ratio: float
    circuits: int
    estimated_pipe_length_m: float


@dataclass
class ProjectQuantities:
    """High level summary for reports/exports."""

    hvac: List[HVACRecommendation]
    plumbing: PlumbingQuantities
    underfloor: UnderfloorHeatingQuantities


@dataclass
class SymbolClassDefinition:
    """Definition entry for YOLO training/class mapping."""

    name: str
    index: int
    description: str


@dataclass
class DatasetTemplate:
    """Describes how to layout a dataset for YOLO training."""

    root_dir: Path
    images_dir: Path
    labels_dir: Path
    class_map: List[SymbolClassDefinition]

