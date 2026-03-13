from claudedev_shared import greet


def test_greet() -> None:
    assert greet("Project Alpha") == "Hello from claudedev_shared, Project Alpha!"