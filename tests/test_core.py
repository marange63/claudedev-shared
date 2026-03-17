from claudedev_shared import greet, ubs_live_price_holdings, ubs_401k_holdings


def test_greet() -> None:
    assert greet("Project Alpha") == "Hello from claudedev_shared, Project Alpha!"


def test_load_ubs_holdings() -> None:
    df = ubs_live_price_holdings()
    df2 = ubs_401k_holdings()
    assert not df.empty
    assert {"DESCRIPTION", "SYMBOL", "SOD VALUE"}.issubset(df.columns)
    i = 0  # breakpoint here
