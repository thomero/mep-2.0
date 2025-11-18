"""CLI helper to run symbol detection on a folder of images."""
from __future__ import annotations

import argparse
from pathlib import Path

from app.core.models import PageImage
from app.core.symbol_detector import SymbolDetector


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect MEP symbols on prepared PNGs")
    parser.add_argument("images", type=Path, help="Directory with PNG files")
    parser.add_argument("--model", type=Path, required=False)
    parser.add_argument("--classes", type=Path, required=False)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    class_names = args.classes.read_text().splitlines() if args.classes and args.classes.exists() else None
    detector = SymbolDetector(model_path=args.model, class_names=class_names)
    images = [
        PageImage(page_number=i + 1, image_path=path, width=0, height=0)
        for i, path in enumerate(sorted(args.images.glob("*.png")))
    ]
    detections = detector.detect(images)
    for det in detections:
        print(det)


if __name__ == "__main__":
    main()

