"""FastAPI interface for the MEP extraction service."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from app.core.pipeline import MEPExtractionPipeline
from app.core.models import ProjectQuantities

app = FastAPI(title="MEP Extraction API", version="1.0.0")
LOGGER = logging.getLogger(__name__)
pipeline = MEPExtractionPipeline()


@app.post("/analyze")
async def analyze_plan(file: UploadFile = File(...)) -> Dict[str, str]:
    temp_dir = Path("/tmp/mep")
    temp_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = temp_dir / file.filename
    pdf_path.write_bytes(await file.read())
    export_paths = pipeline.run(pdf_path, temp_dir / pdf_path.stem)
    return {key: str(path) for key, path in export_paths.items()}


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(Exception)
async def exception_handler(request, exc: Exception):  # type: ignore[override]
    LOGGER.exception("Unhandled error")
    return JSONResponse(status_code=500, content={"detail": str(exc)})

