from src.pygrowwapi.model import Candle
from datetime import datetime


def test_candle_from_raw():
    """Test Candle.from_raw correctly maps values."""
    raw = [1700000000, 100, 110, 95, 105, 1000]  # mock candle
    candle = Candle.from_raw(raw)

    assert isinstance(candle, Candle)
    assert candle.open == 100
    assert candle.close == 105
    assert candle.volume == 1000
    assert isinstance(candle.timestamp, datetime)
