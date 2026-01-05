# examples/agent_loop.py
from praxis import Client

client = Client(api_key="praxis-demo-key")

state = {
    "position": {"x": 0, "y": 0},
    "goal": {"x": 5, "y": 5},
}

for step in range(3):
    nav = client.navigation.plan(
        start=state["position"],
        goal=state["goal"],
    )

    path = nav.data.get("path", [])
    if not path:
        print("No path found")
        break

    # Move agent along first step
    state["position"] = path[0]

    print(
        f"Step {step}: moved to {state['position']} "
        f"(cost={nav.cost})"
    )
