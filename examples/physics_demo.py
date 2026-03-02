# examples/physics_demo.py
from praxis import Client

# Get your API key from https://dashboard.prraas.tech/
client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")

print("=== Force Demo ===")
cases = [(1, 9.8), (2, 3), (5, 1.5)]
for m, a in cases:
    res = client.physics.force(mass=m, acceleration=a)
    print(f"  m={m}, a={a} -> F={res.data['force']} N (cost={res.cost})")

print("\n=== Collision Demo ===")
# Two overlapping boxes
box_a = {"x": 0, "y": 0, "z": 0, "w": 2, "h": 2, "d": 2}
box_b = {"x": 1, "y": 1, "z": 1, "w": 2, "h": 2, "d": 2}
res = client.physics.collision(box_a=box_a, box_b=box_b)
print(f"  Colliding: {res.data['colliding']}")
print(f"  Penetration: {res.data['penetration']}")
print(f"  MTV: {res.data['min_translation_vector']}")

# Two separated boxes
box_c = {"x": 10, "y": 10, "z": 10, "w": 1, "h": 1, "d": 1}
res2 = client.physics.collision(box_a=box_a, box_b=box_c)
print(f"  Separated boxes colliding: {res2.data['colliding']}")

print("\n=== Drag Resistance Demo ===")
# A drone moving at 15 m/s in air
res = client.physics.resistance(
    velocity=15.0,
    drag_coefficient=0.47,
    cross_sectional_area=0.05,
)
print(f"  Drone drag at 15 m/s: {res.data['drag_force']} N (cost={res.cost})")
