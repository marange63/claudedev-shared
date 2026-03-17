from claudedev_shared import greet, ubs_live_price_holdings


def test_greet() -> None:
    assert greet("Project Alpha") == "Hello from claudedev_shared, Project Alpha!"


def test_load_ubs_holdings() -> None:
    df = ubs_live_price_holdings()
    print(df.head)
    i = 0  # breakpoint here