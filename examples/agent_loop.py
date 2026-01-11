# examples/agent_loop.py
"""
Demonstrates agent navigation through a grid with waypoints.
Uses Praxis A* pathfinding API for deterministic route planning.
"""
from praxis import Client

# Get your API key from https://dashboard.prraas.tech/
client = Client(
    api_key="praxis-demo-key",
    base_url="https://api.prraas.tech"
)

# 8x8 grid with obstacles (0 = passable, 1 = blocked)
grid = [
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 0],
]

waypoints = [(0, 0), (4, 5), (7, 7)]
position = waypoints[0]
total_cost = 0.0

for i in range(1, len(waypoints)):
    goal = waypoints[i]
    print(f"\nNavigating: {position} -> {goal}")
    
    while position != goal:
        res = client.navigation.plan(grid=grid, start=position, goal=goal)
        result = res.data.get("result", res.data)
        path = result.get("path", [])
        total_cost += res.cost
        
        if len(path) < 2:
            break
        
        position = tuple(path[1])
        print(f"  {tuple(path[0])} -> {position}")

    print(f"Reached: {goal}")

print(f"\nTotal cost: ${total_cost:.4f}")
