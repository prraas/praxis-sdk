# examples/physics_demo.py
from praxis import Client

# Get your API key from https://dashboard.prraas.tech/
client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")

cases = [
    (1, 9.8),
    (2, 3),
    (5, 1.5),
]

for mass, acc in cases:
    res = client.physics.force(mass=mass, acceleration=acc)
    print(f"m={mass}, a={acc} -> F={res.data['force']} (cost={res.cost})")
