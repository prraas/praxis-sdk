# tests/test_navigation.py
from praxis import Client


def test_navigation_plan():
    client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")

    # 5x5 grid with no obstacles
    grid = [[0 for _ in range(5)] for _ in range(5)]

    res = client.navigation.plan(
        grid=grid,
        start=(0, 0),
        goal=(4, 4),
    )

    result = res.data.get("result", res.data)

    assert res.success is True
    assert result.get("reachable") is True
    assert "path" in result
    assert isinstance(result["path"], list)
    assert res.cost > 0
