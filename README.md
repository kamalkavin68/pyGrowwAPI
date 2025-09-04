# pyGrowwAPI

📈 **Unofficial Python client for Groww Stock Market Data (NSE).**

Easily fetch **live quotes** and **historical OHLCV candles** for Indian stocks using Groww's web APIs.

---

## 🚀 Installation

```bash
pip install pyGrowwAPI
```

---

## 📌 Quick Start

```python
from pyGrowwAPI.client import GrowwClient

# Initialize client
client = GrowwClient()

# Get live stock quotes
quotes = client.get_quotes("SBIN")
print(quotes)

# Get historical OHLCV data
candles = client.history_price("SBIN", "30day", "1day")
for c in candles[:5]:
    print(c.timestamp, c.open, c.close)
```

---

## 🔹 API Documentation

### `GrowwClient`

Main client to interact with Groww's API.

---

#### `get_quotes(symbol: str) -> dict`

Fetch the latest OHLC (Open, High, Low, Close) and other market data for a stock.

- **symbol** (`str`): Stock symbol, e.g., `"SBIN"`, `"TCS"`.  
- **returns**: `dict` JSON response with latest prices.

---

#### `history_price(symbol: str, range_period: str, interval: str) -> list[Candle]`

Fetch historical candlestick (OHLCV) data for a stock.

- **symbol** (`str`): Stock symbol, e.g., `"SBIN"`, `"INFY"`.  
- **range_period** (`str`): Time span of data.  
  - Format → `"<number><unit>"`  
  - Units: `day`, `week`, `month`, `year`  
  - Examples: `"30day"`, `"2week"`, `"6month"`, `"5year"`  
- **interval** (`str`): Candlestick interval.  
  - Format → `"<number><unit>"`  
  - Units: `min`, `hour`, `day`, `week`, `month`, `year`  
  - Examples: `"1min"`, `"15min"`, `"1hour"`, `"1day"`  
- **returns**: `list[Candle]`

---

### `Candle` Model

Represents a single OHLCV (Open, High, Low, Close, Volume) candle.

| Attribute  | Type      | Description                 |
|------------|-----------|-----------------------------|
| timestamp  | datetime  | Candle start time (IST)     |
| open       | float     | Opening price               |
| high       | float     | Highest price               |
| low        | float     | Lowest price                |
| close      | float     | Closing price               |
| volume     | int       | Traded volume               |

---

## ✅ Examples

### Fetching 5 years of daily candles

```python
candles = client.history_price("TCS", "5year", "1day")
print(len(candles))  # number of daily candles
```

### Fetching intraday 15-minute candles

```python
candles = client.history_price("INFY", "7day", "15min")
for c in candles[:10]:
    print(c.timestamp, c.close)
```

---

## ⚠️ Disclaimer

- This package uses **Groww’s public endpoints**, which are **undocumented**.  
- Groww may change or restrict these APIs at any time.  
- Use this package for **educational / personal projects** only.  

---

## 📜 License

MIT License © 2025 Your Name
