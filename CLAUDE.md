# claudedev-shared

Shared Python library used across multiple ClaudeDev PyCharm projects.

## Package structure

```
src/claudedev_shared/
    __init__.py       # public API exports
    core.py           # all functions (greet, UBS holdings pipeline, 401K pipeline)
tests/
    test_core.py
pyproject.toml
```

## Key functions (core.py)

| Function | Purpose |
|---|---|
| `load_raw_ubs_holdings(path)` | Reads UBS_Holdings.csv, selects DESCRIPTION/SYMBOL/VALUE/CHANGE IN VALUE, parses currency strings to float, computes SOD VALUE = VALUE - CHANGE IN VALUE |
| `ubs_live_price_holdings(tickers_path)` | Filters raw holdings (drops NaN symbols, excludes `_EXCLUDED_DESCRIPTIONS`), groups by DESCRIPTION+SYMBOL summing VALUE and SOD VALUE, merges with Ticker-Aliases.csv, drops VALUE. Pure transformation — no save. |
| `load_raw_ubs_401k(path)` | Reads UBS 401K.csv, parses currency columns, renames Fund Name→DESCRIPTION and Opening Balance→SOD VALUE, sets SYMBOL=DESCRIPTION, keeps only DESCRIPTION/SYMBOL/SOD VALUE |
| `ubs_401k_holdings(tickers_path)` | Merges raw 401K holdings with Ticker-Aliases-401K.csv on DESCRIPTION+SYMBOL. Pure transformation — no save. |
| `save_ubs_live_price_holdings(df, path)` | Saves a DataFrame to CSV — separated from transformation logic |
| `_parse_currency(series)` | Strips `$`, commas, whitespace; converts `(1,234.56)` → `-1234.56`; returns float Series |
| `_DATA_DIR` | Base path for all data files: `C:\Users\wamfo\ClaudeDev\data` |
| `_EXCLUDED_DESCRIPTIONS` | List of description substrings to filter out: `["CLOVER", "UBS", "NINETEEN77"]` |

## Data files (local only, not in repo)

All data lives under `C:\Users\wamfo\ClaudeDev\data\`:

| File | Role |
|---|---|
| `UBS_Holdings.csv` | Source holdings export from UBS. Currency columns use `$1,234.56` and `(1,234.56)` format for negatives. |
| `Ticker-Aliases.csv` | Maps DESCRIPTION+SYMBOL pairs to ticker metadata for UBS holdings. Joined on both columns. |
| `UBS 401K.csv` | Source 401K export from UBS. Same currency format. |
| `Ticker-Aliases-401K.csv` | Maps DESCRIPTION+SYMBOL pairs to ticker metadata for 401K holdings. Joined on both columns. |
| `ubs_live_price_holdings.csv` | Output file written by `save_ubs_live_price_holdings`. |

## Conventions

- Currency strings in the CSV use `$`, comma thousands separators, and parentheses for negatives — always use `_parse_currency()` to convert them.
- Exclusion list is `_EXCLUDED_DESCRIPTIONS` in `core.py` — add new patterns there, not inline.
- All data paths are built from `_DATA_DIR` using `os.path.join` — never hardcode full paths in function signatures.
- All transformation functions are pure (no save side effects); saving is a separate explicit step via `save_ubs_live_price_holdings`.
- The pattern for each data source is: `load_raw_*` (read + normalise) and a separate `*_holdings` (filter/merge/transform).
- All DataFrames use `reset_index(drop=True)` after filtering to keep indices clean for the PyCharm DataFrame viewer.
- Tests import from `claudedev_shared` (the public API), never from `claudedev_shared.core` directly.
