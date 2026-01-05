# examples/session_demo.py
from robostream import Client

client = Client(api_key="robostream-demo-key")

with client.session() as session:
    f1 = session.physics.force(1, 2)
    f2 = session.physics.force(3, 4)

    print("F1:", f1.data, "cost:", f1.cost)
    print("F2:", f2.data, "cost:", f2.cost)
