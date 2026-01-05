# 🤝 Contributing to PRAXIS

PRAXIS is infrastructure.
Clarity, correctness, and determinism matter more than clever abstractions.

We welcome contributions that improve the system responsibly.

---

## 📌 What You Can Contribute

We actively welcome:

- New reasoning domains (physics, navigation, simulation)
- SDK ergonomics improvements
- Documentation improvements
- Test coverage
- Bug fixes related to determinism, cost tracking, or correctness

We are less interested in:

- UI-only changes
- speculative abstractions
- non-deterministic behavior
- convenience shortcuts that reduce transparency

---

## 🧠 Design Principles (Non-Negotiable)

All contributions must respect:

1. **Determinism**
   - Same input → same output
   - No hidden randomness

2. **Explicitness**
   - Costs must be visible
   - Errors must be explicit

3. **Minimalism**
   - No unnecessary abstractions
   - Prefer readable code over clever code

4. **Infra Mindset**
   - This is not an app
   - This is a protocol & execution layer

---

## 🛠 Development Setup

```bash
git clone https://github.com/prraas/praxis-sdk.git
cd praxis-sdk
python -m venv venv
source venv/bin/activate
pip install -e .
````

Run tests before submitting:

```bash
pytest
```

---

## 📐 Coding Guidelines

* Python ≥ 3.10
* Type hints required for public interfaces
* Docstrings for public APIs
* No breaking changes without discussion
* Deterministic behavior is mandatory

---

## 🔁 Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make focused, minimal changes
4. Add tests if behavior changes
5. Submit a PR with a clear description

PRs without a clear rationale may be rejected.

---

## 🚫 What Will Be Rejected

* Breaking API changes without justification
* Non-deterministic logic
* Hidden state or implicit behavior
* Hard-coded costs or magic values
* Over-engineering

---

## 🧭 Final Note

PRAXIS is building **Robotics Reasoning as a Service**.

This requires discipline, not hype.

If you value:

* correctness
* reproducibility
* long-term infrastructure

You’ll fit right in.

Welcome.

---