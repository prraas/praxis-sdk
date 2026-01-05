# tests/test_navigation.py
from robostream import Client


def test_navigation_plan():
    client = Client(api_key="robostream-demo-key")

    res = client.navigation.plan(
        start={"x": 0, "y": 0},
        goal={"x": 5, "y": 5},
    )

    assert res.success is True
    assert "path" in res.data
    assert isinstance(res.data["path"], list)
    assert res.cost > 0
