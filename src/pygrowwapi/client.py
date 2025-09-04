from __future__ import annotations

import requests
from datetime import datetime, timedelta
from .model import Candle, MarketDepth

class GrowwClient:
    """
    Client for fetching stock market data from Groww's unofficial API.
    """

    BASE_URL: str = "https://groww.in/v1/api"
    QUOTES_URL: str = BASE_URL + "/stocks_data/v1/accord_points/exchange/NSE/segment/CASH/latest_prices_ohlc/{symbol}"
    HISTORY_URL: str = BASE_URL + "/charting_service/v2/chart/exchange/NSE/segment/CASH/{symbol}"
    DEPTH_URL: str = BASE_URL + "/stocks_data/v1/tr_live_book/exchange/NSE/segment/CASH/{symbol}/latest"

    VALID_PERIOD_UNITS = ["day", "week", "month", "year"]
    VALID_INTERVAL_UNITS = ["min", "hour", "day", "week", "month", "year"]

    def __init__(self) -> None:
        """Initialize the Groww client."""
        pass

    def get_quotes(self, symbol: str) -> dict:
        """Fetch the latest OHLC quotes for the stock symbol."""
        url = self.QUOTES_URL.format(symbol=symbol.upper())
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def history_price(self, symbol: str, range_period: str, interval: str) -> list[Candle]:
        """
        Fetch historical OHLCV (candlestick) data.

        Args:
            symbol (str): Stock symbol (e.g., "SBIN", "TCS").
            range_period (str): Period like "30day", "2week", "6month", "5year".
            interval (str): Interval like "1min", "15min", "1hour", "1day".

        Returns:
            list[Candle]: List of Candle objects.
        """
        period_value, period_unit = self._parse_period(range_period)
        interval_minutes = self._parse_interval(interval)

        days = period_value * {
            "day": 1,
            "week": 7,
            "month": 30,
            "year": 365,
        }[period_unit]

        now = datetime.now()
        start_date = now - timedelta(days=days)

        params = {
            "startTimeInMillis": int(start_date.timestamp() * 1000),
            "endTimeInMillis": int(now.timestamp() * 1000),
            "intervalInMinutes": interval_minutes,
        }

        url = self.HISTORY_URL.format(symbol=symbol.upper())
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        raw_candles = resp.json().get("candles", [])

        return [Candle.from_raw(c) for c in raw_candles]

    def _parse_period(self, period: str) -> tuple[int, str]:
        """Parse a period like '30day' or '2year'."""
        for unit in self.VALID_PERIOD_UNITS:
            if period.endswith(unit):
                try:
                    return int(period.replace(unit, "")), unit
                except ValueError:
                    raise ValueError(f"Invalid number in period: {period}")
        raise ValueError(
            f"Invalid period format: {period}. Use a number followed by one of {', '.join(self.VALID_PERIOD_UNITS)}"
        )

    def _parse_interval(self, interval: str) -> int:
        """Parse an interval like '15min' or '2hour' into minutes."""
        mapping = {
            "min": 1,
            "hour": 60,
            "day": 1440,
            "week": 1440 * 7,
            "month": 1440 * 30,
            "year": 1440 * 365,
        }
        for unit in self.VALID_INTERVAL_UNITS:
            if interval.endswith(unit):
                try:
                    value = int(interval.replace(unit, ""))
                except ValueError:
                    raise ValueError(f"Invalid number in interval: {interval}")
                return value * mapping[unit]
        raise ValueError(
            f"Invalid interval format: {interval}. Use a number followed by one of {', '.join(self.VALID_INTERVAL_UNITS)}"
        )

    def get_market_depth(self, symbol: str) -> MarketDepth:
        """
        Fetch live order book (market depth) for the stock.

        Args:
            symbol (str): NSE stock symbol (e.g., "SBIN").

        Returns:
            MarketDepth: Parsed market depth model with buy/sell books.
        """
        url = self.DEPTH_URL.format(symbol=symbol.upper())
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        raw = resp.json()
        return MarketDepth(**raw)