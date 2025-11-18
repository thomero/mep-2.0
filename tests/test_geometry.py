import json
from pathlib import Path

from app.core.geometry_extractor import GeometryExtractor


def test_geometry_extractor_assigns_labels(tmp_path: Path):
    data_path = Path("tests/data/sample_plan_vectors.json")
    sample = json.loads(data_path.read_text())
    extractor = GeometryExtractor(min_room_area=1)
    rooms = extractor.from_vectors(sample)
    rooms = extractor.assign_labels(rooms, sample[0]["text_items"])
    labels = sorted(room.label for room in rooms if room.label)
    assert labels == ["Bedroom 1", "Kitchen"]
    assert all(room.area_sqm > 5 for room in rooms)

