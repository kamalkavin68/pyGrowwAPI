import pytest
import responses
from src.pygrowwapi.client import GrowwClient
from src.pygrowwapi.model import Candle


@responses.activate
def test_get_quotes_success():
    """Test get_quotes returns mocked JSON."""
    url = GrowwClient.QUOTES_URL.format(symbol="SBIN")
    mock_response = {"SBIN": {"last_price": 123.45}}

    responses.add(
        responses.GET,
        url,
        json=mock_response,
        status=200,
    )

    client = GrowwClient("SBIN")
    result = client.get_quotes()

    assert "SBIN" in result
    assert result["SBIN"]["last_price"] == 123.45


@responses.activate
def test_history_price_success():
    """Test history_price returns a list of Candle objects."""
    url = GrowwClient.HISTORY_URL.format(symbol="SBIN")
    mock_response = {
        "candles": [
            # timestamp (ms), open, high, low, close, volume
            [1700000000, 100, 110, 95, 105, 1000],
            [1700000600, 105, 115, 100, 110, 1200],
        ]
    }

    responses.add(
        responses.GET,
        url,
        json=mock_response,
        status=200,
    )

    client = GrowwClient("SBIN")
    candles = client.history_price("1day", "1min")

    assert isinstance(candles, list)
    assert all(isinstance(c, Candle) for c in candles)
    assert candles[0].open == 100
    assert candles[1].close == 110


def test_parse_period_valid():
    """Test valid period parsing."""
    client = GrowwClient("SBIN")
    value, unit = client._parse_period("30day")
    assert value == 30
    assert unit == "day"

    value, unit = client._parse_period("2week")
    assert value == 2
    assert unit == "week"


def test_parse_period_invalid():
    """Test invalid period raises ValueError."""
    client = GrowwClient("SBIN")
    with pytest.raises(ValueError):
        client._parse_period("10xyz")


def test_parse_interval_valid():
    """Test valid interval parsing."""
    client = GrowwClient("SBIN")
    assert client._parse_interval("1min") == 1
    assert client._parse_interval("2hour") == 120
    assert client._parse_interval("1day") == 1440


def test_parse_interval_invalid():
    """Test invalid interval raises ValueError."""
    client = GrowwClient("SBIN")
    with pytest.raises(ValueError):
        client._parse_interval("10lightyear")
