# 🚀 PRAXIS SDK - Usage Guide

### *Robotics Reasoning as a Service (RRaaS)*

This document explains how to use the **PRAXIS SDK** in real-world robotics
and agent-based workflows.

It covers:

* core SDK concepts
* domain APIs (physics, navigation, simulation)
* response handling
* session-based reasoning
* cost awareness
* recommended usage patterns

This is the **most important document** for SDK users.

If you understand this file, you understand how to use PRAXIS correctly.

---

## 🧠 Core Mental Model

Before writing any code, it helps to understand how PRAXIS is designed.

PRAXIS separates **reasoning execution** from your local system.

You do **not** run robotics computation locally.
You **request execution** from PRAXIS.

Every interaction follows the same pattern:

```
Input + Intent
      ↓
PRAXIS Execution
      ↓
Result + Cost + Trace
```

Everything in the SDK is built around this model.

---

## 🧩 Core SDK Concepts

There are only three concepts you need to learn:

### 1. Client

The main entry point into PRAXIS.

### 2. Domain APIs

Physics, navigation, and simulation reasoning surfaces.

### 3. Response Objects

Structured, transparent execution results.

Nothing else is hidden.

---

## 🧠 Creating a Client

The `Client` object is the main interface to PRAXIS.

```python
from praxis import Client

client = Client(
    api_key="rbs_prod_...",
    base_url="https://api.prraas.tech"
)
```

### API Key Resolution

If the API key is not passed explicitly, the SDK will attempt to read it from:

```bash
PRAXIS_API_KEY
```

Environment variables are **recommended** for production systems.

---

## 🧭 Domain APIs Overview

Once a client is created, domain APIs are exposed as properties:

* `client.physics`
* `client.navigation`
* `client.simulation`

Each domain API exposes **deterministic reasoning methods**.

---

## ⚙️ Physics API

The Physics API evaluates physical relationships and constraints.

### Example: Force Calculation

```python
res = client.physics.force(mass=2, acceleration=3)
print(res.data)   # {'force': 6.0}
print(res.cost)   # 0.001
```

### Example: Collision Detection

Check if two 3D objects occupy the same space:

```python
box_a = {"x": 0, "y": 0, "z": 0, "w": 2, "h": 2, "d": 2}
box_b = {"x": 1, "y": 1, "z": 1, "w": 2, "h": 2, "d": 2}

res = client.physics.collision(box_a=box_a, box_b=box_b)

if res.data["colliding"]:
    mtv = res.data["min_translation_vector"]
    print(f"Collision on axis {mtv['axis']}, depth {mtv['depth']}m")
```

### Example: Drag Resistance

Calculate aerodynamic force acting on a moving object:

```python
res = client.physics.resistance(
    velocity=15.0,           # m/s
    drag_coefficient=0.47,   # sphere
    cross_sectional_area=0.05,
)
print(f"Drag force: {res.data['drag_force']} N")
```

### Example: Arm Leverage

Evaluate joint safety for a robotic arm lift:

```python
res = client.physics.leverage(
    arm_length=1.5,
    angle_degrees=45,
    load_mass=10.0,
    pivot_torque_limit=150
)

print(f"Torque: {res.data['torque_exerted']} Nm")
if res.data["exceeds_limit"]:
    print("WARNING: Pivot torque limit exceeded!")
```

Physics execution is:

* deterministic
* stateless (unless used in a session)
* fully traceable

---

## 🧭 Navigation API

The Navigation API handles path planning and navigation reasoning.

### Example: Grid-Based Path Planning

```python
# Create a 10x10 grid (0 = passable, 1 = obstacle)
grid = [[0 for _ in range(10)] for _ in range(10)]
grid[3][4] = 1  # Add obstacle
grid[6][7] = 1

res = client.navigation.plan(
    grid=grid,
    start=(0, 0),
    goal=(9, 9)
)
```

### Result Structure

```python
result = res.data.get("result", res.data)
print(result)
```

Example:

```python
{
  "reachable": True,
  "steps": 18,
  "path": [[0,0], [0,1], ...]
}
```

Navigation results are:

* deterministic
* environment-consistent
* reproducible across machines

### Example: Trajectory Smoothing

Smooth out jerky, grid-based paths into natural movement trajectories:

```python
# discrete input path
path = [(0,0), (1,1), (2,0)]

res = client.navigation.smooth_path(
    path=path,
    density=5  # generate 5 points between each waypoint
)

# smoothed_path is a list of [x, y] coordinates
smoothed_path = res.data
```

---

## 👁️ Vision & Spatial Mapping API

The Vision API provides high-precision instance segmentation and spatial reasoning.

### Example: Instance Segmentation

Identify precise object shapes and their functional roles in the scene:

```python
# Image data as base64
img_b64 = "..."

res = client.vision.segment(
    image=img_b64,
    model_tier="nano",
    min_confidence=0.5
)

for obj in res.data["objects"]:
    print(f"Object: {obj['label']} | Role: {obj['role']}")
    print(f"Points: {len(obj['points'])} vertices")
```

### Advanced: Spatial Utilities

The SDK includes `spatial_utils` for processing vision results:

```python
from praxis.core.spatial_utils import calculate_polygon_area, is_point_in_polygon

# Find the floor/navigable surface
floor = next(o for o in res.data["objects"] if o["role"] == "navigable_surface")

# Calculate area to ensure robot fits
area = calculate_polygon_area(floor["points"])

# Check if a specific target coordinate is safe
is_safe = is_point_in_polygon(0.5, 0.9, floor["points"])
```

---

## 🧪 Simulation API

The Simulation API validates robotic logic through controlled execution.

### Example: Navigation Simulation

```python
grid = [[0 for _ in range(10)] for _ in range(10)]

res = client.simulation.navigate(
    grid=grid,
    start=(0, 0),
    goal=(9, 9)
)
```

### Reading Simulation Output

```python
result = res.data.get("result", res.data)
print(result)
```

Example:

```python
{
  "reachable": True,
  "steps": 18,
  "path": [[0, 0], [0, 1], ...]
}
```

Simulation execution is designed for:

* validation
* sanity checks
* agent decision verification

---

## ✋ Manipulation & Sorting

### Example: Pick Planning

```python
res = client.manipulation.pick(
    object_position=[1.0, 0.0, 0.5],
    gripper_position=[1.0, 0.0, 0.6],
    object_size=[0.1, 0.2, 0.1],
    gripper_opening=0.15,
    object_material="steel"
)

if res.success:
    print("Safe to pick!")
else:
    print("Slippage detected:", res.data["warnings"])
```

### Example: Grasp Feasibility

Check if a gripper can securely hold an object of a given size:

```python
res = client.manipulation.grasp_feasibility(
    object_width=0.08,
    gripper_max_aperture=0.12
)

if res.data["feasible"]:
    print(f"Perfect match! Feasibility score: {res.data['score']}")
```

### Example: Grasp Robustness

Score how resistant a grasp is to external disturbances:

```python
res = client.manipulation.grasp_robustness(
    contact_forces=[[0.0, 0.0, 5.0], [0.0, 0.0, -5.0]],
    object_mass=0.5
)
print(f"Robustness score: {res.data['robustness_score']}")
```

### Example: Sorting Logic

```python
items = [
    {"id": "apple", "color": "red"},
    {"id": "banana", "color": "yellow"}
]
bins = [
    {"id": "red_bin", "criteria": "red", "capacity": 10},
    {"id": "yellow_bin", "criteria": "yellow", "capacity": 10}
]

res = client.sorting.sort(items, bins, "color")
print(res.data["placements"])
```

---

## 🤖 Multi-Agent Coordination API

The Multi-Agent API enables coordination logic for fleets of robots operating in shared environments.

### Example: Trajectory Conflict Detection

Detect whether two agents will collide along their paths:

```python
res = client.multi_agent.check_conflicts(
    trajectories=[
        [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [2, 0, 0]]
    ],
    threshold=0.5
)
print(f"Conflicts detected: {res.data['conflict_count']}")
```

### Example: Swarm Steering

Compute a steering vector to guide an agent toward a target while avoiding others:

```python
res = client.multi_agent.swarm_steer(
    agent_position=[1.0, 1.0, 0.0],
    target_position=[5.0, 5.0, 0.0],
    neighbor_positions=[[1.5, 1.0, 0.0], [1.0, 1.5, 0.0]]
)
print(f"Steering vector: {res.data['steering_vector']}")
```

### Example: Formation Planning

Arrange a fleet of agents into a geometric formation:

```python
res = client.multi_agent.formation(
    agent_count=4,
    formation_type="line",
    spacing=1.5
)
print(f"Positions: {res.data['positions']}")
```

---

## 📦 Response Object

Every SDK call returns a **Response** object.

This object is **not** a raw dictionary.

### Response Fields

| Field        | Description                            |
| ------------ | -------------------------------------- |
| `success`    | Whether execution succeeded            |
| `data`       | Result payload                         |
| `cost`       | Cost charged for this execution        |
| `request_id` | Unique, traceable execution identifier |

### Example

```python
res = client.physics.force(2, 3)

if res.success:
    print(res.data)
else:
    print("Execution failed")
```

PRAXIS always returns **explicit execution metadata**.

---

## 🔁 Using Sessions (Agent Workflows)

Sessions allow grouping multiple executions into a **single logical workflow**.

This is especially useful for:

* agent loops
* multi-step planning
* chained reasoning
* decision pipelines

### Example: Session Workflow

```python
grid = [[0 for _ in range(10)] for _ in range(10)]

with client.session() as session:
    r1 = session.physics.force(1, 2)
    r2 = session.physics.force(3, 4)
    r3 = session.navigation.plan(
        grid=grid,
        start=(0, 0),
        goal=(5, 5)
    )

print(r1.data["force"], r1.cost)
print(r2.data["force"], r2.cost)
print(r3.data, r3.cost)
```

Inside a session:

* execution context is shared
* request tracing is consistent
* reasoning remains deterministic

Each call is still **billed independently**.

---

## 🔍 Cost Awareness (By Design)

Every execution returns a `cost`.

```python
res = client.physics.force(2, 3)
print(res.cost)
```

PRAXIS does **not** hide costs.

This enables:

* budget-aware agents
* explicit accounting
* programmable limits
* economic reasoning

Cost transparency is a core design principle.

---

## 🚨 Error Handling

PRAXIS fails **loudly and explicitly**.

Typical error categories include:

* authentication errors
* invalid input / validation errors
* execution failures
* quota or balance limits
* disabled API keys

### Example

```python
try:
    res = client.physics.force(2, -1)
except Exception as e:
    print(type(e), e)
```

Errors are raised immediately.
Silent failures are treated as bugs.

---

## 🧪 Determinism Guarantees

PRAXIS guarantees deterministic execution.

This means:

* identical inputs → identical outputs
* no hidden randomness
* no environment drift
* reproducible experiments

This is critical for:

* debugging
* research validation
* agent verification
* paid reasoning systems

---

## 🧠 Recommended Usage Patterns

### Pattern 1: Single Execution

Use direct calls for isolated reasoning tasks.

### Pattern 2: Session-Based Pipelines

Use sessions for agent loops and chained decisions.

### Pattern 3: Batch Reasoning

Loop over inputs and collect responses programmatically.

PRAXIS does not restrict workflow structure.

---

## ⚠️ Common Mistakes

* Forgetting to set the API key
* Using unsupported Python versions
* Treating response objects as dictionaries
* Ignoring execution cost
* Assuming hidden state outside sessions

---

## 📌 Summary

The PRAXIS SDK is designed to be:

* explicit
* deterministic
* composable
* production-oriented

Use direct calls for simple reasoning.
Use sessions for structured workflows.

PRAXIS exposes execution clearly - **nothing is hidden**.

---