# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.2.0] - 2025-09-04
### Changed
- Converted `GrowwClient` methods to accept `symbol` as a parameter instead of in constructor.
- Improved documentation for `history_price()` and `get_quotes()`.
- Updated README.md with installation and usage examples.
- Added `.gitignore` and `LICENSE` file.

---

## [0.1.0] - 2025-09-03
### Added
- Initial release of `pyGrowwAPI`.
- `GrowwClient` with:
  - `get_quotes(symbol)` → fetch live quotes
  - `history_price(symbol, range_period, interval)` → fetch OHLCV candles
- `Candle` model with Pydantic support.
