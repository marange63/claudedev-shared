from claudedev_shared import greet, load_raw_ubs_holdings


def test_greet() -> None:
    assert greet("Project Alpha") == "Hello from claudedev_shared, Project Alpha!"


def test_load_ubs_holdings() -> None:
    df = load_raw_ubs_holdings()
    print(df.head)
    i = 0  # breakpoint here