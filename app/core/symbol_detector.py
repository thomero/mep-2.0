"""YOLO based symbol detection wrapper."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Iterable, List, Optional

try:  # pragma: no cover
    from ultralytics import YOLO
except Exception:  # pragma: no cover
    YOLO = None  # type: ignore

from app.core.models import PageImage, SymbolDetection

LOGGER = logging.getLogger(__name__)


class SymbolDetector:
    def __init__(self, model_path: Optional[Path] = None, class_names: Optional[List[str]] = None) -> None:
        self.model_path = model_path
        self.class_names = class_names or []
        self._model = YOLO(str(model_path)) if (YOLO and model_path and model_path.exists()) else None

    def detect(self, images: Iterable[PageImage]) -> List[SymbolDetection]:
        detections: List[SymbolDetection] = []
        for image in images:
            if not self._model:
                LOGGER.warning("YOLO model unavailable; skipping detection")
                continue
            results = self._model(str(image.image_path))
            for res in results:
                boxes = res.boxes.xyxy.tolist()
                scores = res.boxes.conf.tolist()
                classes = res.boxes.cls.tolist()
                for bbox, score, cls_idx in zip(boxes, scores, classes):
                    label = self._resolve_label(int(cls_idx))
                    detections.append(SymbolDetection(label, float(score), tuple(bbox), image.page_number))
        return detections

    def _resolve_label(self, class_index: int) -> str:
        if not self.class_names:
            return f"class_{class_index}"
        if class_index < len(self.class_names):
            return self.class_names[class_index]
        return self.class_names[-1]

    @staticmethod
    def save_detections(detections: List[SymbolDetection], out_path: Path) -> None:
        payload = [det.__dict__ for det in detections]
        out_path.write_text(json.dumps(payload, indent=2))

