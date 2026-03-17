"""Core shared functions."""

import pandas as pd


def greet(project_name: str) -> str:
    """Return a friendly message proving the shared package import worked."""
    return f"Hello from claudedev_shared, {project_name}!"


def load_raw_ubs_holdings(path: str = r"C:\Users\wamfo\ClaudeDev\data\UBS_Holdings.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[["DESCRIPTION", "SYMBOL", "VALUE"]]
    df["VALUE"] = pd.to_numeric(df["VALUE"].str.replace(r"[$,]", "", regex=True).str.strip(), errors="coerce")
    return df

def ubs_live_price_holdings():
    df = load_raw_ubs_holdings()
    df = df[df["SYMBOL"].notna()].reset_index(drop=True)
    df = df[~df["DESCRIPTION"].str.contains("CLOVER|UBS|NINETEEN77", na=False)].reset_index(drop=True)
    df = df.groupby(["DESCRIPTION", "SYMBOL"], as_index=False)["VALUE"].sum()
    df.to_csv(r"C:\Users\wamfo\ClaudeDev\data\ubs_live_price_holdings.csv", index=False)
    return df
