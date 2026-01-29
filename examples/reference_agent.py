# examples/reference_agent.py
"""
Reference Agent Implementation (Phase 1 Lock-In)

Status: Stable Reference
Guarantee: Deterministic Execution

This reference implementation demonstrates a robust, deterministic agent loop
using the PRAXIS v1-alpha API. It handles locking behavior, explicit failure
states, and verifiable decision making.
"""
from praxis import Client

# Get your API key from https://dashboard.prraas.tech/
client = Client(
    api_key="praxis-demo-key",
    base_url="https://api.prraas.tech"
)

def run_deterministic_agent():
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

    print("Starting Reference Agent Loop (v1-alpha)...")

    for i in range(1, len(waypoints)):
        goal = waypoints[i]
        print(f"\nNavigating: {position} -> {goal}")
        
        while position != goal:
            # Deterministic API Call
            res = client.navigation.plan(grid=grid, start=position, goal=goal)
            
            # Explicit Error Handling
            if not res.success:
                print(f"CRITICAL FAILURE: Reasoning engine returned error. Request ID: {res.request_id}")
                return

            result = res.data.get("result", res.data)
            path = result.get("path", [])
            total_cost += res.cost
            
            # "Cannot Decide" / No Path Logic
            if not path:
                print(f"STOP: No path found to {goal}. Agent halted.")
                return

            if len(path) < 2:
                # We are at the goal
                break
            
            # Move one step deterministically
            next_step = tuple(path[1])
            print(f"  Move: {position} -> {next_step} [Req: {res.request_id}]")
            position = next_step

        print(f"Goal Reached: {goal}")

    print(f"\nReasoning Complete.")
    print(f"Total Compute Cost: ${total_cost:.4f}")
    print("Agent shut down safely.")

if __name__ == "__main__":
    run_deterministic_agent()
