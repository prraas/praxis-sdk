# examples/quickstart.py
from robostream import Client

# API key can also come from env ROBOSTREAM_API_KEY
client = Client(api_key="robostream-demo-key")

res = client.physics.force(mass=2, acceleration=3)

print("Force:", res.data)
print("Cost:", res.cost)
print("Request ID:", res.request_id)
