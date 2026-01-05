# examples/quickstart.py
from praxis import Client

client = Client(api_key="praxis-demo-key")

res = client.physics.force(mass=2, acceleration=3)

print("Force:", res.data)
print("Cost:", res.cost)
print("Request ID:", res.request_id)
