# examples/physics_demo.py
from robostream import Client

client = Client(api_key="robostream-demo-key")

cases = [
    (1, 9.8),
    (2, 3),
    (5, 1.5),
]

for mass, acc in cases:
    res = client.physics.force(mass=mass, acceleration=acc)
    print(f"m={mass}, a={acc} → F={res.data['force']} (cost={res.cost})")
