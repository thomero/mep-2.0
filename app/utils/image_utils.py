"""Image helpers for raster processing."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np

try:  # pragma: no cover
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore


def resize_image(image_path: Path, target_size: Tuple[int, int]) -> Path:
    if cv2 is None:
        raise RuntimeError("OpenCV not installed")
    image = cv2.imread(str(image_path))
    resized = cv2.resize(image, target_size)
    out_path = image_path.with_name(image_path.stem + f"_{target_size[0]}x{target_size[1]}.png")
    cv2.imwrite(str(out_path), resized)
    return out_path

