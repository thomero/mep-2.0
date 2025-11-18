from __future__ import annotations

import argparse
from pathlib import Path

from app.core.pipeline import MEPExtractionPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the MEP extraction pipeline")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    pipeline = MEPExtractionPipeline()
    result = pipeline.run(args.pdf, args.output)
    for key, path in result.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()

