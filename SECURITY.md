# 🔐 Security Policy — PRAXIS

PRAXIS is infrastructure software.
Security, determinism, and correctness are treated as first-class requirements.

This document describes how to report vulnerabilities and what to expect.

---

## 📌 Supported Components

Security reviews apply to:

- PRAXIS SDK
- PRAXIS backend / API
- Authentication & API key handling
- Billing & usage enforcement
- Deterministic execution guarantees

Frontend/UI issues without security impact are out of scope.

---

## 🚨 Reporting a Vulnerability

If you discover a security issue, **do not open a public issue**.

Instead, report it privately.

### 📬 Contact

Email: **security@prraas.tech**  
Subject: **[SECURITY] Vulnerability Report**

Include:

- A clear description of the issue
- Steps to reproduce
- Potential impact
- Affected components (SDK, API, billing, etc.)

Proof-of-concepts are appreciated but not required.

---

## ⏱ Response Timeline

We aim to:

- Acknowledge reports within **48 hours**
- Provide an initial assessment within **5 business days**
- Release fixes as soon as reasonably possible

Critical vulnerabilities may result in temporary feature restriction.

---

## 🧠 Security Philosophy

PRAXIS follows these principles:

- **Explicit failures over silent compromise**
- **Determinism over hidden state**
- **Least-privilege API key enforcement**
- **Auditability over convenience**

Security issues affecting correctness, determinism, or billing
are treated as **high severity**.

---

## 🛡 Responsible Disclosure

We support responsible disclosure and will credit reporters
unless anonymity is requested.

No legal action will be taken against good-faith researchers
who follow this policy.

---

Thank you for helping keep PRAXIS secure.
