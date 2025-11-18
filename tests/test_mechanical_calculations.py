from app.core.hvac_calculator import HVACCalculator
from app.core.models import RoomGeometry, SymbolDetection
from app.core.plumbing_calculator import PlumbingCalculator
from app.core.underfloor_calculator import UnderfloorCalculator
from app.utils.simple_polygon import SimplePolygon


def build_room(room_id: str, label: str, x0: float, y0: float, width: float, height: float):
    polygon = SimplePolygon(
        [
            (x0, y0),
            (x0 + width, y0),
            (x0 + width, y0 + height),
            (x0, y0 + height),
        ]
    )
    area_sqm = polygon.area / 10000.0
    return RoomGeometry(room_id=room_id, polygon=polygon, area_sqm=area_sqm, label=label, attributes={"category": label})


def test_hvac_and_plumbing_quantities():
    rooms = [
        build_room("r1", "bedroom", 0, 0, 400, 300),
        build_room("r2", "kitchen", 500, 0, 300, 300),
    ]
    hvac_calc = HVACCalculator()
    hvac = hvac_calc.recommendations(rooms)
    assert len(hvac) == 2
    assert hvac[0].required_btus > 0

    plumbing_calc = PlumbingCalculator()
    symbols = [
        SymbolDetection(label="WC", confidence=0.9, bbox=(0, 0, 1, 1), page_number=1),
        SymbolDetection(label="Kitchen Sink", confidence=0.9, bbox=(0, 0, 1, 1), page_number=1),
    ]
    plumbing = plumbing_calc.summarize(rooms, symbols)
    assert plumbing.sewage_points == 2
    assert plumbing.hot_water_points == 1 + 0  # sink + wc rule

    underfloor = UnderfloorCalculator().summarize(rooms)
    assert underfloor.total_area_sqm > 0
    assert underfloor.heated_area_sqm <= underfloor.total_area_sqm

