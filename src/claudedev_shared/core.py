"""Core shared functions."""

import os
import pandas as pd

_DATA_DIR = r"C:\Users\wamfo\ClaudeDev\data"
_EXCLUDED_DESCRIPTIONS = ["CLOVER", "UBS", "NINETEEN77"]


def greet(project_name: str) -> str:
    """Return a friendly message proving the shared package import worked."""
    return f"Hello from claudedev_shared, {project_name}!"


def _parse_currency(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.str.replace(r"[$,]", "", regex=True)
              .str.strip()
              .str.replace(r"^\((.+)\)$", r"-\1", regex=True),
        errors="coerce"
    )


def load_raw_ubs_holdings(
    path: str = os.path.join(_DATA_DIR, "UBS_Holdings.csv"),
) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[["DESCRIPTION", "SYMBOL", "VALUE", "CHANGE IN VALUE"]]
    df["VALUE"] = _parse_currency(df["VALUE"])
    df["CHANGE IN VALUE"] = _parse_currency(df["CHANGE IN VALUE"])
    df["SOD VALUE"] = df["VALUE"] - df["CHANGE IN VALUE"]
    return df


def ubs_live_price_holdings(
    tickers_path: str = os.path.join(_DATA_DIR, "Ticker-Aliases.csv"),
) -> pd.DataFrame:
    df = load_raw_ubs_holdings()
    df = df[df["SYMBOL"].notna()].reset_index(drop=True)
    pattern = "|".join(_EXCLUDED_DESCRIPTIONS)
    df = df[~df["DESCRIPTION"].str.contains(pattern, na=False)].reset_index(drop=True)
    df = df.groupby(["DESCRIPTION", "SYMBOL"], as_index=False)[["VALUE", "SOD VALUE"]].sum()
    df_tickers = pd.read_csv(tickers_path)
    df = df.merge(df_tickers, on=["DESCRIPTION", "SYMBOL"], how="left")
    df = df.drop(columns=["VALUE"])
    return df


def load_raw_ubs_401k(
    path: str = os.path.join(_DATA_DIR, "UBS 401K.csv"),
) -> pd.DataFrame:
    df = pd.read_csv(path)
    currency_cols = ["Opening Balance", "Gains/Losses", "Other Activity", "Closing Balance", "Fund Price"]
    for col in currency_cols:
        if col in df.columns:
            df[col] = _parse_currency(df[col])
    df = df.rename(columns={"Fund Name": "DESCRIPTION", "Opening Balance": "SOD VALUE"})
    df["SYMBOL"] = df["DESCRIPTION"]
    df = df[["DESCRIPTION", "SYMBOL", "SOD VALUE"]].reset_index(drop=True)
    return df


def ubs_401k_holdings(
    tickers_path: str = os.path.join(_DATA_DIR, "Ticker-Aliases-401K.csv"),
) -> pd.DataFrame:
    df = load_raw_ubs_401k()
    df_tickers = pd.read_csv(tickers_path)
    df = df.merge(df_tickers, on=["DESCRIPTION", "SYMBOL"], how="left")
    return df


def save_ubs_live_price_holdings(
    df: pd.DataFrame,
    path: str = os.path.join(_DATA_DIR, "ubs_live_price_holdings.csv"),
) -> None:
    df.to_csv(path, index=False)
