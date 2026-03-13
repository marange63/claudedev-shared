"""Core shared functions."""

import pandas as pd


def greet(project_name: str) -> str:
    """Return a friendly message proving the shared package import worked."""
    return f"Hello from claudedev_shared, {project_name}!"


def load_ubs_holdings() -> pd.DataFrame:
    df = pd.read_csv(r"C:\Users\wamfo\ClaudeDev\data\UBS_Holdings.csv")
    df = df[["DESCRIPTION", "SYMBOL", "QUANTITY"]]
    df = df[df["SYMBOL"].notna()].reset_index(drop=True)
    df = df[~df["DESCRIPTION"].str.contains("CLOVER", na=False)].reset_index(drop=True)
    return df
