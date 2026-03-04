from praxis import Client

client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")


# ─────────────────────────────────────────────
# force()
# ─────────────────────────────────────────────

def test_force_calculation():
    res = client.physics.force(mass=2, acceleration=3)

    assert res.success is True
    assert "force" in res.data
    assert res.data["force"] == 6.0
    assert res.cost > 0
    assert isinstance(res.request_id, str)


# ─────────────────────────────────────────────
# collision()
# ─────────────────────────────────────────────

def test_collision_overlapping_boxes():
    box_a = {"x": 0, "y": 0, "z": 0, "w": 2, "h": 2, "d": 2}
    box_b = {"x": 1, "y": 1, "z": 1, "w": 2, "h": 2, "d": 2}

    res = client.physics.collision(box_a=box_a, box_b=box_b)

    assert res.success is True
    assert res.data["colliding"] is True
    assert res.data["penetration"]["x"] > 0
    assert res.data["min_translation_vector"]["axis"] is not None
    assert res.cost > 0


def test_collision_separated_boxes():
    box_a = {"x": 0,  "y": 0,  "z": 0,  "w": 1, "h": 1, "d": 1}
    box_b = {"x": 10, "y": 10, "z": 10, "w": 1, "h": 1, "d": 1}

    res = client.physics.collision(box_a=box_a, box_b=box_b)

    assert res.success is True
    assert res.data["colliding"] is False
    assert res.data["penetration"]["x"] == 0.0
    assert res.cost > 0


# ─────────────────────────────────────────────
# resistance()
# ─────────────────────────────────────────────

def test_resistance_basic():
    res = client.physics.resistance(
        velocity=10.0,
        drag_coefficient=0.47,
        cross_sectional_area=1.0,
    )

    assert res.success is True
    assert "drag_force" in res.data
    assert res.data["drag_force"] > 0
    assert res.data["fluid_density"] == 1.225
    assert res.cost > 0


def test_resistance_zero_velocity():
    res = client.physics.resistance(
        velocity=0.0,
        drag_coefficient=0.47,
        cross_sectional_area=1.0,
    )

    assert res.success is True
    assert res.data["drag_force"] == 0.0


