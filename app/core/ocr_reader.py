"""OCR utilities to detect room labels on rasterized pages."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List

try:  # pragma: no cover
    from paddleocr import PaddleOCR
except Exception:  # pragma: no cover
    PaddleOCR = None  # type: ignore

from app.core.models import PageImage

LOGGER = logging.getLogger(__name__)


class OCRReader:
    def __init__(self, lang: str = "en") -> None:
        self.lang = lang
        self._ocr = PaddleOCR(use_angle_cls=True, lang=lang) if PaddleOCR else None

    def read(self, images: List[PageImage]) -> Dict[int, List[str]]:
        """Return words detected on each page."""

        outputs: Dict[int, List[str]] = {}
        for page in images:
            if not self._ocr:
                LOGGER.warning("PaddleOCR unavailable; returning empty result")
                outputs[page.page_number] = []
                continue
            result = self._ocr.ocr(str(page.image_path), cls=True)
            outputs[page.page_number] = [item[1][0] for line in result for item in line]
        return outputs

