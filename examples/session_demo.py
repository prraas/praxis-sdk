# examples/session_demo.py
from praxis import Client

# Get your API key from https://dashboard.prraas.tech/
client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")

with client.session() as session:
    f1 = session.physics.force(1, 2)
    f2 = session.physics.force(3, 4)

    print("F1:", f1.data["force"], "cost:", f1.cost)
    print("F2:", f2.data["force"], "cost:", f2.cost)
