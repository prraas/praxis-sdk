# 🧠 PRAXIS SDK

### **Robotics Reasoning as a Service (RRaaS)**

> **PRAXIS gives AI agents the ability to reason about the physical world - navigation, physics, simulation, and structured decision logic - delivered through simple, deterministic APIs.**

PRAXIS is **infrastructure**, not an application.  
It provides **deterministic robotic reasoning** as a paid, composable execution layer for AI agents, autonomous systems, and developer platforms.

---

## 📌 Table of Contents

1. [What Is PRAXIS](#-what-is-praxis)  
2. [Why PRAXIS Exists](#-why-praxis-exists)  
3. [What This SDK Provides](#-what-this-sdk-provides)  
4. [Who This Is For](#-who-this-is-for)  
5. [Core Concepts](#-core-concepts)  
6. [Supported Reasoning Domains](#-supported-reasoning-domains)  
7. [Documentation](#-documentation)  
8. [Installation](#-installation)  
9. [Authentication](#-authentication)  
10. [Quick Start](#-quick-start)  
11. [Sessions & Agent Workflows](#-sessions--agent-workflows)  
12. [Response Model](#-response-model)  
13. [Determinism Guarantee](#-determinism-guarantee)  
14. [Error Handling](#-error-handling)  
15. [Architecture Overview](#-architecture-overview)  
16. [Examples](#-examples)  
17. [Project Status](#-project-status)  
18. [Philosophy](#-philosophy)  
19. [Contributing](#-contributing)  
20. [Links](#-links)  
21. [License](#-license)

---

## 🧠 What Is PRAXIS

**PRAXIS is a Robotics Reasoning as a Service (RRaaS) protocol.**

It exposes **robotic reasoning primitives** - physics evaluation, navigation logic, simulation validation, and structured decision steps - through **deterministic, metered APIs**.

PRAXIS does **not**:

- control robots  
- train models  
- replace ROS or simulators  

PRAXIS **executes reasoning**.

Think of PRAXIS as:

- 🧠 *Reasoning compute for agents*  
- ⚙️ *Execution infrastructure for physical-world logic*  
- 💸 *Pay-per-use intelligence*  

---

## 🌍 Why PRAXIS Exists

Robotic reasoning today is:

- tightly coupled to hardware  
- buried inside simulators  
- non-deterministic across environments  
- difficult to reproduce  
- impossible to monetize cleanly  

This blocks:

- agent reliability  
- infrastructure standardization  
- economic coordination  

**PRAXIS separates reasoning from hardware and tooling** and turns it into a **standardized execution layer**.

> Just as Stripe abstracted payments and AWS abstracted compute,  
> **PRAXIS abstracts robotic reasoning.**

---

## 🚀 What This SDK Provides

The PRAXIS SDK is the **official Python client** for the PRAXIS RRaaS platform.

With this SDK you can:

- call robotic reasoning APIs from Python  
- execute physics, navigation, and simulation remotely  
- build multi-step agent workflows  
- track execution cost per call  
- trace every request with a unique ID  

The SDK is intentionally **thin, explicit, and deterministic**.

---

## 👥 Who This Is For

This SDK is designed for:

- AI agent developers  
- robotics & simulation engineers  
- infrastructure teams building autonomous systems  
- crypto-native agent protocols  
- research teams requiring reproducibility  

It is **not** intended for consumer robotics applications or UI-driven tools.

---

## 🧩 Core Concepts

### RRaaS - Robotics Reasoning as a Service

PRAXIS treats reasoning as:

- callable  
- deterministic  
- metered  
- composable  

Reasoning is **not free**, **not hidden**, and **not probabilistic**.

---

### Deterministic Execution

- same input → same output  
- no hidden randomness  
- no environment drift  
- no silent version changes  

---

### Transparency

Every request returns:

- execution result  
- cost charged  
- traceable request ID  

Nothing is implicit.

---

## ⚙️ Supported Reasoning Domains

PRAXIS currently supports:

- ⚙️ **Physics reasoning**  
- 🧭 **Navigation & path logic**  
- 🧪 **Simulation & validation**  
- 🔁 **Multi-step agent workflows**  

New domains can be added without breaking existing integrations.

---

## 📚 Documentation

PRAXIS documentation is intentionally split into **four focused files**:

```

docs/
├── overview.md
├── installation.md
├── api-reference.md
└── usage.md

````

### 📘 [`overview.md`](https://github.com/prraas/praxis-sdk/blob/main/docs/overview.md)
High-level explanation of PRAXIS, RRaaS, system architecture, and design philosophy.

### 📦 [`installation.md`](https://github.com/prraas/praxis-sdk/blob/main/docs/installation.md)
Environment requirements, SDK installation, API key setup, and verification steps.

### 📜 [`api-reference.md`](https://github.com/prraas/praxis-sdk/blob/main/docs/api-reference.md)
Formal API specification: methods, parameters, response schemas, cost semantics, and errors.

### 🧪 [`usage.md`](https://github.com/prraas/praxis-sdk/blob/main/docs/usage.md)
Practical examples: basic calls, sessions, agent loops, and integration patterns.

---

## 📦 Installation

### Requirements

- Python **3.10+**

### Install (Git-based)

```bash
git clone https://github.com/prraas/praxis-sdk.git
cd praxis-sdk
pip install -e .
````

Git-based installation is intentional for transparency and auditability.

---

## 🔐 Authentication

PRAXIS uses **API keys** issued from the PRAXIS Utility Dashboard.

### Environment Variable (Recommended)

```bash
export PRAXIS_API_KEY=your-api-key
```

### Or in Code

```python
from praxis import Client
client = Client(api_key="your-api-key")
```

API keys enforce access control, usage limits, and billing.

---

## ⚡ Quick Start

```python
from praxis import Client

client = Client()

res = client.physics.force(mass=2, acceleration=3)

print(res.data)        # {'force': 6.0}
print(res.cost)        # execution cost
print(res.request_id)  # traceable execution ID
```

---

## 🔁 Sessions & Agent Workflows

PRAXIS supports **sessions** for multi-step reasoning.

```python
with client.session() as session:
    r1 = session.physics.force(1, 2)
    r2 = session.physics.force(3, 4)
```

Notes:

* sessions group logic, not hidden state
* each call is billed independently
* full traceability is preserved

---

## 📦 Response Model

All SDK calls return a structured response:

| Field        | Meaning                |
| ------------ | ---------------------- |
| `success`    | Execution status       |
| `data`       | Result payload         |
| `cost`       | Cost charged           |
| `request_id` | Traceable execution ID |

---

## 🧠 Determinism Guarantee

PRAXIS is deterministic by design:

* same input → same output
* no probabilistic inference
* no hidden state mutation

Suitable for:

* reproducible research
* agent verification
* economic intelligence flows

---

## 🚨 Error Handling

PRAXIS fails **explicitly**.

Error categories include:

* authentication
* validation
* execution
* quota / balance
* disabled API keys

Silent failures are treated as bugs.

---

## 🏗 Architecture Overview

```
Agent / Application
        ↓
PRAXIS SDK
        ↓
PRAXIS RRaaS API
        ↓
Deterministic Reasoning Engine
        ↓
Result + Cost + Request ID
```

---

## 🧪 Examples

See `/examples` for runnable demos:

* `quickstart.py`
* `physics_demo.py`
* `navigation_demo.py`
* `agent_loop.py`
* `session_demo.py`

---

## 📊 Project Status

| Component         | Status            |
| ----------------- | ----------------- |
| Backend           | Stable            |
| SDK               | Stable            |
| Utility Dashboard | Live              |
| Billing           | Demo → Production |
| Open Source       | Yes               |

---

## 🧭 Philosophy

PRAXIS values:

1. Execution over tooling
2. Determinism over convenience
3. Transparency over abstraction
4. Infrastructure over hype

---

## 🌱 Contributing

Contributions are welcome:

* new reasoning domains
* SDK improvements
* documentation
* tests

Clarity beats cleverness.

---

## 🔗 Links

* 🌐 Website: [https://prraas.tech](https://prraas.tech)
* 🧰 Utility Dashboard: [https://dashboard.prraas.tech](https://dashboard.prraas.tech)
* 🐦 Twitter / X: [https://x.com/praxis_rraas](https://x.com/praxis_rraas)
* 📖 Docs: [https://docs.prraas.tech](https://docs.prraas.tech/)

---

## 📄 License

MIT License - free to use, modify, and build upon.

---