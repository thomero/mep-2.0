# MEP 2.0 – Automated Quantity Extraction

End-to-end Python platform that ingests architectural PDFs and produces mechanical, electrical, and plumbing (MEP) quantities with engineering-grade accuracy. The solution combines PDF vector parsing, OCR, YOLO-based symbol detection, and HVAC/plumbing calculation heuristics while exposing a FastAPI interface and multiple export formats.

## Features

- **PDF ingestion**: Handles raster/vector plans using PyMuPDF and pdfplumber.
- **Geometry extraction**: Builds room polygons, walls, and boundaries with Shapely-compatible primitives.
- **OCR**: Uses PaddleOCR to read room labels and associate semantics.
- **Symbol detection**: Custom YOLOv8/v9 pipeline for WC, basins, showers, AC units, radiators, floor drains, etc.
- **MEP calculations**:
  - HVAC BTU sizing with Cyprus climate factors.
  - Plumbing fixture counting and pipe length estimation.
  - Underfloor heating usable area, circuits, and pipe requirements.
- **Exports**: JSON data lake, CSV BOQ, and PDF summary reports.
- **API ready**: FastAPI server with `/analyze` endpoint for integrations.
- **Tests**: Pytest suite validates the critical math modules.

## Project Structure

```
app/
  api/                 # FastAPI entrypoint
  core/                # PDF parsing, OCR, geometry, calculations
  ai/                  # YOLO configs, training helpers
  output/              # Export utilities
  utils/               # Shared helpers + shapely fallback
  ...
tests/                # Pytest suites + sample vector data
data/examples/        # Dataset template for YOLO training
```

## Installation

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. (Optional) Install system packages for PaddleOCR/Tesseract/Poppler depending on OS as described in their documentation.

## Running the FastAPI Service

```bash
uvicorn app.api.main:app --reload
```

Upload a PDF via `POST /analyze` using curl or any HTTP client:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@/path/to/plan.pdf"
```

The response contains paths to the generated JSON, CSV, and PDF reports.

## CLI Pipeline Execution

```bash
python -m app.core.pipeline /path/to/plan.pdf output/
```

To expose a convenient entry point, create a small runner script invoking `MEPExtractionPipeline().run(...)`.

## Training the YOLO Detector

1. Prepare your dataset following `data/examples/dataset_template.md` and map classes via `app/ai/models/classes.txt`.
2. Update `app/ai/models/yolo_config.yaml` with actual dataset paths.
3. Launch training:

```bash
python app/ai/train_yolo.py app/ai/models/yolo_config.yaml yolov8n.pt --epochs 150 --img 1024
```

4. After training, place the resulting weights (e.g., `runs/detect/train/weights/best.pt`) in a secure location and reference it via `SymbolDetector(model_path=...)`.

## Example Dataset Template

See `data/examples/dataset_template.md` for folder layout and YOLO label formatting. The repository includes `tests/data/sample_plan_vectors.json` for validating vector parsing logic without requiring heavy PDFs.

## Unit Tests

Run the full suite with:

```bash
pytest
```

Tests cover geometry extraction, HVAC sizing, plumbing aggregation, and underfloor heating calculations.

## Output Artifacts

After running the pipeline you will find:

- `output.json` – structured data for downstream systems.
- `output.csv` – bill of quantities ready for spreadsheets.
- `summary.pdf` – printable engineering summary.

## FastAPI Response Contract

```json
{
  "json": "/tmp/mep/plan/output.json",
  "csv": "/tmp/mep/plan/output.csv",
  "pdf": "/tmp/mep/plan/summary.pdf"
}
```

## Example PDF Parsing Test Case

`tests/data/sample_plan_vectors.json` mirrors a minimal floor plan with bedrooms and kitchens. The pytest suite loads this file to verify that room labels are assigned and areas computed, serving as an executable documentation example for implementing full PDF parsing.

## Docker (optional)

To containerize, add a `Dockerfile` installing system dependencies and run `uvicorn app.api.main:app`. A docker-compose stack can front the API with Nginx for production deployments.

## Contributing

- Format code with `black`/`isort` (optional but recommended).
- Add unit tests for each new module.
- Document new configuration flags in this README.

## License

MIT
