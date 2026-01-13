# examples/quickstart.py
from praxis import Client

# Get your API key from https://dashboard.prraas.tech/
client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")

res = client.physics.force(mass=2, acceleration=3)

print("Force:", res.data["force"])
print("Cost:", res.cost)
print("Request ID:", res.request_id)
