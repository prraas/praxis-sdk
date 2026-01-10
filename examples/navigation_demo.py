# examples/navigation_demo.py
from praxis import Client

# Get your API key from https://dashboard.prraas.tech/
client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")

# Create a 15x15 grid (0 = passable, 1 = obstacle)
grid = [[0 for _ in range(15)] for _ in range(15)]

# Add some obstacles
grid[5][5] = 1
grid[5][6] = 1
grid[5][7] = 1
grid[6][5] = 1
grid[7][5] = 1

# Define start and goal positions (row, col)
start = (0, 0)
goal = (10, 10)

res = client.navigation.plan(
    grid=grid,
    start=start,
    goal=goal,
)

# Access the result inside data
result = res.data.get("result", res.data)

print("Reachable:", result.get("reachable"))
print("Steps:", result.get("steps"))
print("Path:", result.get("path"))
print("Cost:", res.cost)
