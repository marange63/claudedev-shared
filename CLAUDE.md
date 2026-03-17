# claudedev-shared

Shared Python library used across multiple ClaudeDev PyCharm projects.

## Package structure

```
src/claudedev_shared/
    __init__.py       # public API exports
    core.py           # all functions (greet, UBS holdings pipeline)
tests/
    test_core.py
pyproject.toml
```

## Key functions (core.py)

| Function | Purpose |
|---|---|
| `load_raw_ubs_holdings(path)` | Reads UBS_Holdings.csv, selects DESCRIPTION/SYMBOL/VALUE/CHANGE IN VALUE, parses currency strings to float, computes SOD VALUE = VALUE - CHANGE IN VALUE |
| `ubs_live_price_holdings(tickers_path)` | Filters raw holdings (drops NaN symbols, excludes `_EXCLUDED_DESCRIPTIONS`), groups by DESCRIPTION+SYMBOL summing VALUE and SOD VALUE, merges with Ticker-Aliases.csv, drops VALUE, saves output CSV |
| `save_ubs_live_price_holdings(df, path)` | Saves a DataFrame to CSV — separated from transformation logic |
| `_parse_currency(series)` | Strips `$`, commas, whitespace; converts `(1,234.56)` → `-1234.56`; returns float Series |
| `_EXCLUDED_DESCRIPTIONS` | List of description substrings to filter out: `["CLOVER", "UBS", "NINETEEN77"]` |

## Data files (local only, not in repo)

All data lives under `C:\Users\wamfo\ClaudeDev\data\`:

| File | Role |
|---|---|
| `UBS_Holdings.csv` | Source holdings export from UBS. Currency columns use `$1,234.56` and `(1,234.56)` format for negatives. |
| `Ticker-Aliases.csv` | Maps DESCRIPTION+SYMBOL pairs to additional ticker metadata. Joined on both columns. |
| `ubs_live_price_holdings.csv` | Output file written by `save_ubs_live_price_holdings`. |

## Conventions

- Currency strings in the CSV use `$`, comma thousands separators, and parentheses for negatives — always use `_parse_currency()` to convert them.
- Exclusion list is `_EXCLUDED_DESCRIPTIONS` in `core.py` — add new patterns there, not inline.
- `ubs_live_price_holdings` is a pure transformation; saving is a separate explicit step via `save_ubs_live_price_holdings`.
- All DataFrames use `reset_index(drop=True)` after filtering to keep indices clean for the PyCharm DataFrame viewer.
- Tests import from `claudedev_shared` (the public API), never from `claudedev_shared.core` directly.
