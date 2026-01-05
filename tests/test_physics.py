# tests/test_physics.py
from praxis import Client


def test_force_calculation():
    client = Client(api_key="praxis-demo-key")

    res = client.physics.force(mass=2, acceleration=3)

    assert res.success is True
    assert "force" in res.data
    assert res.data["force"] == 6.0
    assert res.cost > 0
    assert isinstance(res.request_id, str)
