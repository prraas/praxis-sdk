# tests/test_sessions.py
from robostream import Client


def test_session_context():
    client = Client(api_key="robostream-demo-key")

    with client.session() as session:
        r1 = session.physics.force(1, 2)
        r2 = session.physics.force(3, 4)

        assert r1.success is True
        assert r2.success is True
        assert r1.cost > 0
        assert r2.cost > 0
