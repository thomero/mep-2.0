"""Utility script to train YOLOv8/v9 for symbol detection."""
from __future__ import annotations

import argparse
from pathlib import Path

try:  # pragma: no cover
    from ultralytics import YOLO
except Exception:  # pragma: no cover
    YOLO = None  # type: ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train YOLO detector for MEP symbols")
    parser.add_argument("config", type=Path, help="Path to YOLO dataset config")
    parser.add_argument("model", type=str, default="yolov8n.pt", nargs="?", help="Base model weight")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--img", type=int, default=640)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if YOLO is None:
        raise RuntimeError("ultralytics is not installed")
    model = YOLO(args.model)
    model.train(data=str(args.config), epochs=args.epochs, imgsz=args.img)


if __name__ == "__main__":
    main()

