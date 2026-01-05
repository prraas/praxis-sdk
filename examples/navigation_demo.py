# examples/navigation_demo.py
from robostream import Client

client = Client(api_key="robostream-demo-key")

start = {"x": 0, "y": 0}
goal = {"x": 10, "y": 10}
obstacles = [
    {"x": 5, "y": 5, "radius": 1},
]

res = client.navigation.plan(
    start=start,
    goal=goal,
    obstacles=obstacles,
)

print("Path:", res.data.get("path"))
print("Cost:", res.cost)
