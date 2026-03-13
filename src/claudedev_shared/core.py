"""Core shared functions."""

import pandas as pd


def greet(project_name: str) -> str:
    """Return a friendly message proving the shared package import worked."""
    return f"Big Hello from claudedev_shared, {project_name}!"


def load_ubs_holdings() -> pd.DataFrame:
    return pd.read_csv(r"C:\Users\wamfo\ClaudeDev\data\UBS_Holdings.csv")
