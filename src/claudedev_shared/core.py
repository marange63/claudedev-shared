"""Core shared functions."""

import pandas as pd


def greet(project_name: str) -> str:
    """Return a friendly message proving the shared package import worked."""
    return f"Hello from claudedev_shared, {project_name}!"


def load_raw_ubs_holdings(path: str = r"C:\Users\wamfo\ClaudeDev\data\UBS_Holdings.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[["DESCRIPTION", "SYMBOL", "VALUE", "CHANGE IN VALUE"]]
    df["VALUE"] = pd.to_numeric(df["VALUE"].str.replace(r"[$,]", "", regex=True).str.strip().str.replace(r"^\((.+)\)$", r"-\1", regex=True), errors="coerce")
    df["CHANGE IN VALUE"] = pd.to_numeric(df["CHANGE IN VALUE"].str.replace(r"[$,]", "", regex=True).str.strip().str.replace(r"^\((.+)\)$", r"-\1", regex=True), errors="coerce")
    df["SOD VALUE"] = df["VALUE"] - df["CHANGE IN VALUE"]
    return df

def ubs_live_price_holdings():
    df = load_raw_ubs_holdings()
    df = df[df["SYMBOL"].notna()].reset_index(drop=True)
    df = df[~df["DESCRIPTION"].str.contains("CLOVER|UBS|NINETEEN77", na=False)].reset_index(drop=True)
    df = df.groupby(["DESCRIPTION", "SYMBOL"], as_index=False)[["VALUE", "SOD VALUE"]].sum()
    df.to_csv(r"C:\Users\wamfo\ClaudeDev\data\ubs_live_price_holdings.csv", index=False)
    df_tickers = pd.read_csv(r"C:\Users\wamfo\ClaudeDev\data\Ticker-Aliases.csv")
    df = df.merge(df_tickers, on=["DESCRIPTION", "SYMBOL"], how="left")
    df = df.drop(columns=["VALUE"])
    return df
