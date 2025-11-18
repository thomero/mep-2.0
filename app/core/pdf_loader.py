"""Utilities for reading PDF floor plans and creating analysis-ready artifacts."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

try:  # pragma: no cover - optional dependency
    import fitz  # type: ignore
except Exception:  # pragma: no cover - degrade gracefully
    fitz = None  # type: ignore

try:  # pragma: no cover
    import pdfplumber  # type: ignore
except Exception:  # pragma: no cover
    pdfplumber = None  # type: ignore

from app.core.models import ExtractionResult, PageImage
from app.utils.file_utils import ensure_dir, hash_file

LOGGER = logging.getLogger(__name__)


@dataclass
class PDFPageVectorData:
    """Stores vector extraction results for a PDF page."""

    page_number: int
    shapes: List[dict]
    text_items: List[dict]


class PDFLoader:
    """Loads PDF documents using PyMuPDF/pdfplumber and prepares assets."""

    def __init__(self, raster_dpi: int = 300, cache_dir: Optional[Path] = None) -> None:
        self.raster_dpi = raster_dpi
        self.cache_dir = cache_dir or Path(".cache/pages")
        ensure_dir(self.cache_dir)

    def load(self, pdf_path: Path) -> ExtractionResult:
        LOGGER.info("Loading PDF %s", pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(pdf_path)

        pages = list(self._iterate_pages(pdf_path))
        result = ExtractionResult(file_path=pdf_path, metadata={"page_count": str(len(pages))})
        result.metadata["file_hash"] = hash_file(pdf_path)
        result.metadata["raster_cache"] = str(self.cache_dir)
        return result

    def _iterate_pages(self, pdf_path: Path) -> Iterable[PDFPageVectorData]:
        if pdfplumber is None:
            LOGGER.warning("pdfplumber is not installed; vector extraction disabled")
            return []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_words() if hasattr(page, "extract_words") else []
                vector_content = page.objects
                yield PDFPageVectorData(
                    page_number=page.page_number,
                    shapes=vector_content,
                    text_items=text,
                )

    def rasterize(self, pdf_path: Path) -> List[PageImage]:
        """Rasterize pages to PNG for CV tasks, caching results."""

        if fitz is None:
            LOGGER.warning("PyMuPDF is not installed; rasterization skipped")
            return []

        doc = fitz.open(pdf_path)
        outputs: List[PageImage] = []
        for page_index in range(len(doc)):
            page = doc[page_index]
            pix = page.get_pixmap(dpi=self.raster_dpi)
            out_path = self.cache_dir / f"{pdf_path.stem}_page{page_index+1}.png"
            pix.save(out_path)
            outputs.append(PageImage(page_index + 1, out_path, pix.width, pix.height, self.raster_dpi))
            LOGGER.debug("Rasterized page %s -> %s", page_index + 1, out_path)
        return outputs

    def export_vector_cache(self, vector_data: Iterable[PDFPageVectorData], out_path: Path) -> Path:
        """Persist raw vector extraction for debugging/training datasets."""

        ensure_dir(out_path.parent)
        payload = [dataclass_to_dict(page) for page in vector_data]
        out_path.write_text(json.dumps(payload, indent=2))
        LOGGER.info("Vector cache saved to %s", out_path)
        return out_path


def dataclass_to_dict(page: PDFPageVectorData) -> dict:
    return {"page_number": page.page_number, "shapes": page.shapes, "text_items": page.text_items}

