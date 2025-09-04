from __future__ import annotations

from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional


class Candle(BaseModel):
    """Represents a single OHLCV (Open-High-Low-Close-Volume) candle."""

    timestamp: datetime
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    volume: Optional[int]

    @classmethod
    def from_raw(cls, raw: list) -> "Candle":
        """
        Convert raw candle list from Groww API into a Candle model.

        Args:
            raw (list): [timestamp, open, high, low, close, volume]

        Returns:
            Candle: Pydantic model of a candle.
        """
        # Convert UNIX (ms) timestamp to IST datetime
        ist_datetime = (
            datetime.utcfromtimestamp(raw[0])
            .astimezone()
            + timedelta(hours=5, minutes=30)
        )
        return cls(
            timestamp=ist_datetime,
            open=raw[1],
            high=raw[2],
            low=raw[3],
            close=raw[4],
            volume=raw[5],
        )

