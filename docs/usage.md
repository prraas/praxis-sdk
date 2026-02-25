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
res = client.physics.force(
    mass=2,
    acceleration=3
)
```

### Reading the Result

```python
print(res.success)
print(res.data)
print(res.cost)
print(res.request_id)
```

Example output:

```python
{'force': 6.0}
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