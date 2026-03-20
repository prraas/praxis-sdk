# 📘 PRAXIS API Reference

### *Robotics Reasoning as a Service (RRaaS)*

This document provides the **complete public API reference** for the **PRAXIS SDK**.

It defines:

* exposed classes and interfaces
* available domain APIs
* method signatures and parameters
* response structure
* execution semantics
* error behavior

This document is intended for:

* advanced users
* infrastructure builders
* contributors
* reviewers and auditors

If you are new to PRAXIS, read **`overview.md`** first.

---

## 📦 Top-Level Imports

```python
from praxis import Client
```

> The `praxis` package name is retained for backward compatibility.
> PRAXIS is the protocol and platform name.

---

## 🧠 Client

### Class: `Client`

The `Client` class is the **primary entry point** to the PRAXIS SDK.

It is responsible for:

* API authentication
* HTTP communication
* request lifecycle handling
* exposing domain-specific reasoning APIs

---

### Constructor

```python
Client(
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: float = 10.0
)
```

---

### Parameters

| Name       | Type    | Description                                              |
| ---------- | ------- | -------------------------------------------------------- |
| `api_key`  | `str`   | PRAXIS API key. Optional if set via environment variable |
| `base_url` | `str`   | Base URL of the PRAXIS API (optional)                    |
| `timeout`  | `float` | Request timeout in seconds                               |

If `api_key` is not provided, the SDK reads from:

```bash
PRAXIS_API_KEY
```

---

### Properties

| Property            | Type            | Description               |
| ------------------- | --------------- | ------------------------- |
| `client.physics`    | `PhysicsAPI`    | Physics reasoning API     |
| `client.navigation` | `NavigationAPI` | Navigation & planning API |
| `client.simulation` | `SimulationAPI` | Simulation execution API  |
| `client.manipulation`| `ManipulationAPI` | Object interaction & pick API |
| `client.sorting`    | `SortingAPI`    | Bin packing & rules API   |
| `client.analytics`  | `AnalyticsAPI`  | Telemetry & cost API      |

Each property returns a **domain-specific API object**.

Each property returns a **domain-specific API object**.

---

## ✋ Manipulation API

### Class: `ManipulationAPI`

Accessed via:

```python
client.manipulation
```

The Manipulation API handles **object interaction planning** (picking, placing).

---

### Method: `pick`

```python
pick(
    object_position: list[float],
    gripper_position: list[float],
    object_size: list[float],
    gripper_opening: float,
    object_mass: float = 0.5,
    object_material: str = "plastic"
) -> Response
```

#### Parameters

| Name              | Type           | Description                     |
| ----------------- | -------------- | ------------------------------- |
| `object_position` | `[x, y, z]`    | Center of object                |
| `gripper_position`| `[x, y, z]`    | Center of gripper               |
| `object_size`     | `[w, h, d]`    | Bounding box dimensions         |
| `gripper_opening` | `float`        | Gripper width (meters)          |
| `object_mass`     | `float`        | Mass in kg (default 0.5)        |
| `object_material` | `str`          | "steel", "plastic", "wood", etc |

#### Returns

A `Response` object with `data`:

```json
{
  "success": true,
  "physics": {
    "slippage": false,
    "torque_ok": true
  }
}
```

---

### Method: `grasp_feasibility`

```python
grasp_feasibility(
    object_width: float,
    gripper_max_aperture: float,
    gripper_min_aperture: float = 0.0
) -> Response
```

Assess feasibility of a grasp based on object and gripper geometry.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `object_width` | `float` | Width of the object in meters |
| `gripper_max_aperture` | `float` | Max gripper opening in meters |
| `gripper_min_aperture` | `float` | Min gripper opening in meters (default 0.0) |

#### Returns

A `Response` object with `score` (0.0 - 1.0) and `feasible` (bool).

---

### Method: `grasp_closure`

```python
grasp_closure(
    contacts: list[dict],
    friction_mu: float = 0.4
) -> Response
```

Validate force-closure for a set of contact points.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `contacts` | `list[dict]` | List of contact points with normals `{"x", "y", "nx", "ny"}` |
| `friction_mu` | `float` | Coefficient of friction (default 0.4) |

#### Returns

A `Response` object with `has_closure` status and `score`.

---

## 🗂️ Sorting API

### Class: `SortingAPI`

Accessed via:

```python
client.sorting
```

The Sorting API handles **logical organization and bin packing**.

---

### Method: `sort`

```python
sort(
    items: list[dict],
    bins: list[dict],
    criteria: str
) -> Response
```

#### Parameters

| Name       | Type         | Description                     |
| ---------- | ------------ | ------------------------------- |
| `items`    | `list[dict]` | Objects to sort                 |
| `bins`     | `list[dict]` | available containers with caps  |
| `criteria` | `str`        | Attribute to match ("color")    |

#### Returns

A `Response` object with placement plan.

---

## 📊 Analytics API

### Class: `AnalyticsAPI`

Accessed via:

```python
client.analytics
```

The Analytics API exposes runtime telemetry, cost, and historical logs.

---

### Method: `get_stats`

```python
get_stats(
    days: int = 7,
    endpoint: str | None = None
) -> Response[dict]
```

#### Parameters

| Name       | Type    | Description                     |
| ---------- | ------- | ------------------------------- |
| `days`     | `int`   | Number of past days to query    |
| `endpoint` | `str`   | Optional filter (e.g. "vision") |

#### Returns

A `Response` object containing compute `total_requests`, `total_cost`, `success_rate`, and `endpoints` metrics.

---

### Method: `get_logs`

```python
get_logs(
    limit: int = 50,
    endpoint: str | None = None
) -> Response[dict]
```

#### Returns

A `Response` object containing the `count` and list of recent `logs` with execution timestamps.

---

## ⚙️ Physics API

### Class: `PhysicsAPI`

Accessed via:

```python
client.physics
```

The Physics API exposes **deterministic physical reasoning primitives**.

---

### Method: `force`

```python
force(
    mass: float,
    acceleration: float
) -> Response
```

#### Parameters

| Name           | Type    | Description          |
| -------------- | ------- | -------------------- |
| `mass`         | `float` | Object mass          |
| `acceleration` | `float` | Applied acceleration |

#### Returns

A `Response` object with `data`:

```json
{
  "force": <float>
}
```

#### Example

```python
res = client.physics.force(mass=2, acceleration=3)
```

---

### Method: `mass`

```python
mass(
    volume: float,
    density: float
) -> Response
```

#### Parameters

| Name      | Type    | Description          |
| --------- | ------- | -------------------- |
| `volume`  | `float` | Object volume (m³)   |
| `density` | `float` | Material density (kg/m³) |

#### Returns

A `Response` object with `data`:

```json
{
  "mass": <float>
}
```

---

### Method: `stability`

```python
stability(
    base_width: float,
    center_of_mass_height: float
) -> Response
```

#### Parameters

| Name                    | Type    | Description                   |
| ----------------------- | ------- | ----------------------------- |
| `base_width`            | `float` | Width of the object's base    |
| `center_of_mass_height` | `float` | Height of the center of mass  |

#### Returns

A `Response` object with `data`:

```json
{
  "stability": <float>,
  "warnings": [<str>]
}
```

---

### Method: `collision`

```python
collision(
    box_a: dict,
    box_b: dict
) -> Response
```

Checks whether two 3D axis-aligned bounding boxes (AABB) overlap.

#### Box Format

Each box must have the following keys:

| Key | Description |
|-----|-------------|
| `x`, `y`, `z` | Center position in meters |
| `w`, `h`, `d` | Width, height, depth in meters |

#### Parameters

| Name    | Type   | Description         |
| ------- | ------ | ------------------- |
| `box_a` | `dict` | First bounding box  |
| `box_b` | `dict` | Second bounding box |

#### Returns

A `Response` object with `data`:

```json
{
  "colliding": true,
  "penetration": { "x": 1.0, "y": 1.0, "z": 1.0 },
  "min_translation_vector": { "axis": "x", "depth": 1.0 },
  "warnings": ["Objects are overlapping — collision detected"]
}
```

#### Example

```python
box_a = {"x": 0, "y": 0, "z": 0, "w": 2, "h": 2, "d": 2}
box_b = {"x": 1, "y": 1, "z": 1, "w": 2, "h": 2, "d": 2}

res = client.physics.collision(box_a=box_a, box_b=box_b)
print(res.data["colliding"])     # True
print(res.data["penetration"])   # {"x": 1.0, "y": 1.0, "z": 1.0}
```

---

### Method: `resistance`

```python
resistance(
    velocity: float,
    drag_coefficient: float,
    cross_sectional_area: float,
    fluid_density: float = 1.225
) -> Response
```

Calculates aerodynamic drag force using: **F = 0.5 × ρ × v² × Cd × A**

#### Parameters

| Name                   | Type    | Description                                         |
| ---------------------- | ------- | --------------------------------------------------- |
| `velocity`             | `float` | Object speed in m/s                                 |
| `drag_coefficient`     | `float` | Cd value (e.g. 0.47 for sphere, 1.0 for flat plate) |
| `cross_sectional_area` | `float` | Frontal area in m²                                  |
| `fluid_density`        | `float` | Fluid density in kg/m³ (default: 1.225 = air)       |

#### Returns

A `Response` object with `data`:

```json
{
  "drag_force": 28.7875,
  "velocity": 10.0,
  "drag_coefficient": 0.47,
  "cross_sectional_area": 1.0,
  "fluid_density": 1.225,
  "warnings": null
}
```

#### Example

```python
res = client.physics.resistance(
    velocity=15.0,
    drag_coefficient=0.47,
    cross_sectional_area=0.05,
)
print(res.data["drag_force"])  # N
```

---

### Method: `leverage`

```python
leverage(
    arm_length: float,
    angle_degrees: float,
    load_mass: float,
    pivot_torque_limit: float
) -> Response
```

Calculates mechanical leverage and torque at a specific joint.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `arm_length` | `float` | Length of the arm in meters |
| `angle_degrees` | `float` | Angle of the arm in degrees (0 = horizontal) |
| `load_mass` | `float` | Mass of the load in kg |
| `pivot_torque_limit` | `float` | Max torque limit of the joint in Nm |

#### Returns

A `Response` object with `torque_exerted`, `exceeds_limit`, and `mechanical_advantage`.

---

### Method: `leverage`

```python
leverage(
    arm_length: float,
    angle_degrees: float,
    load_mass: float,
    pivot_torque_limit: float
) -> Response
```

Calculates mechanical leverage and torque at a specific joint.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `arm_length` | `float` | Length of the arm in meters |
| `angle_degrees` | `float` | Angle of the arm in degrees (0 = horizontal) |
| `load_mass` | `float` | Mass of the load in kg |
| `pivot_torque_limit` | `float` | Max torque limit of the joint in Nm |

#### Returns

A `Response` object with `torque_exerted`, `exceeds_limit`, and `mechanical_advantage`.

---


### Class: `VisionAPI`

Accessed via:

```python
client.vision
```

The Vision API provides **visual reasoning and object detection**.

---

### Method: `analyze`

```python
analyze(
    image: str,
    model: str = "auto",
    min_confidence: float = 0.5,
    max_objects: int = 10,
    model_tier: str = "nano"
) -> Response
```

#### Parameters

| Name             | Type    | Description                                      |
| ---------------- | ------- | ------------------------------------------------ |
| `image`          | `str`   | Base64 encoded image string                      |
| `model`          | `str`   | Model selection ("auto", "yolo", "simple")       |
| `min_confidence` | `float` | Minimum confidence threshold (0.0 - 1.0)         |
| `max_objects`    | `int`   | Maximum number of objects to detect              |
| `model_tier`     | `str`   | Execution tier for YOLO ("nano" or "small")      |

#### Returns

A `Response` object with `data` containing detected objects and metadata:

```json
{
  "model": "yolov8",
  "count": 3,
  "objects": [
    {
      "id": 0,
      "label": "person",
      "confidence": 0.95,
      "bbox": {"x": 0.1, "y": 0.1, "width": 0.2, "height": 0.5}
    }
  ]
}
```

---

### Method: `segment`

```python
segment(
    image: str,
    model_tier: str = "nano",
    min_confidence: float = 0.5
) -> Response
```

Perform instance segmentation to identify precise object shapes and spatial roles.

#### Parameters

| Name             | Type    | Description                                      |
| ---------------- | ------- | ------------------------------------------------ |
| `image`          | `str`   | Base64 encoded image string                      |
| `model_tier`     | `str`   | YOLO model tier ("nano" or "small")              |
| `min_confidence` | `float` | Minimum confidence threshold (0.0 - 1.0)         |

#### Returns

A `Response` object with `data` containing polygons and spatial metadata:

```json
{
  "model": "yolov8n-seg",
  "count": 2,
  "objects": [
    {
      "id": 0,
      "label": "floor",
      "role": "navigable_surface",
      "points": [[0.1, 0.8], [0.9, 0.8], ...]
    }
  ],
  "spatial_info": {
    "has_navigable_surface": true,
    "obstacle_count": 1
  }
}
```

---

## 🧭 Navigation API

### Class: `NavigationAPI`

Accessed via:

```python
client.navigation
```

The Navigation API handles **path planning and spatial reasoning**.

---

### Method: `plan`

```python
plan(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int]
) -> Response
```

#### Parameters

| Name    | Type               | Description                          |
| ------- | ------------------ | ------------------------------------ |
| `grid`  | `list[list[int]]`  | 2D grid where 0=passable, 1=obstacle |
| `start` | `tuple[int, int]`  | Start position (row, col)            |
| `goal`  | `tuple[int, int]`  | Goal position (row, col)             |

#### Returns

A `Response` object with `data.result`:

```json
{
  "reachable": true,
  "steps": 10,
  "path": [[0, 0], [0, 1], ...]
}
```

---

## 🧪 Simulation API

### Class: `SimulationAPI`

Accessed via:

```python
client.simulation
```

The Simulation API validates robotics logic through **controlled execution steps**.

---

### Method: `navigate`

```python
navigate(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int]
) -> Response
```

#### Parameters

| Name    | Type               | Description                          |
| ------- | ------------------ | ------------------------------------ |
| `grid`  | `list[list[int]]`  | 2D grid where 0=passable, 1=obstacle |
| `start` | `tuple[int, int]`  | Start position (row, col)            |
| `goal`  | `tuple[int, int]`  | Goal position (row, col)             |

#### Returns

A `Response` object with `data.result`:

```json
{
  "reachable": true,
  "steps": 10,
  "path": [[0, 0], [0, 1], ...]
}
```

---

## 🔁 Sessions

### Method: `Client.session`

```python
session() -> Session
```

Creates a **session context** for grouping multiple executions.

Sessions are useful for:

* agent loops
* multi-step reasoning
* sequential planning
* cost grouping and traceability

---

### Example

```python
with client.session() as session:
    r1 = session.physics.force(1, 2)
    r2 = session.navigation.plan([0, 0], [5, 5])
```

All calls inside a session share:

* execution context
* request grouping
* trace linkage

Each call is **still billed individually**.

---

## 📦 Response Model

### Class: `Response`

All SDK calls return a `Response` object.

---

### Attributes

| Attribute    | Type    | Description                    |
| ------------ | ------- | ------------------------------ |
| `success`    | `bool`  | Whether execution succeeded    |
| `data`       | `dict`  | Computation result payload     |
| `cost`       | `float` | Cost charged for execution     |
| `request_id` | `str`   | Unique, traceable execution ID |

---

### Example

```python
<Response success=True cost=0.001 request_id="...">
```

---

## 🚨 Error Behavior

PRAXIS errors are **explicit and raised immediately**.

Common categories include:

* authentication errors
* invalid input / validation errors
* execution failures
* quota or balance limits
* disabled API keys

Errors are raised as **Python exceptions**.

Silent failures are treated as bugs.

---

## 🔒 Authentication

Authentication is handled automatically by the `Client`.

You do **not** need to manage tokens manually.

API keys are verified server-side and enforced per request.

---

## ⏱ Timeouts

All requests respect the `timeout` value passed to the `Client`.

If execution exceeds this value, a timeout exception is raised.

---

## 🧠 Determinism Guarantee

PRAXIS guarantees:

* same input → same output
* no hidden randomness
* no silent environment drift
* version-controlled execution

Determinism is a **hard protocol requirement**, not a best-effort feature.

---

## 📌 Notes for Contributors

* API surface is intentionally minimal
* Breaking changes require version bumps
* Determinism must never be violated
* Explicitness is preferred over abstraction

---

## 📎 Summary

This document defines the **entire public API surface** of the PRAXIS SDK.

For conceptual grounding, see:

* `overview.md`

For installation steps, see:

* `installation.md`

For real-world usage patterns, see:

* `usage.md`

---