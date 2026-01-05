# 📦 Installation

### *PRAXIS SDK - Robotics Reasoning as a Service (RRaaS)*

This document explains how to install and set up the **PRAXIS SDK**
**directly from source** using Git.

At the current stage, PRAXIS is distributed **only via Git clone**.
There is **no PyPI release yet** .

---

## 🔧 Requirements

Before installing the PRAXIS SDK, ensure the following are available:

* **Python 3.10 or higher**
* `git`
* `pip`
* Internet access (required for API execution)

Verify versions:

```bash
python --version
git --version
pip --version
```

If Python < 3.10, upgrade before proceeding.

---

## 📥 Install from Git (Required)

### 1. Clone the Repository

```bash
git clone https://github.com/prraas/praxis-sdk.git
cd praxis-sdk
```

---

### 2. Create a Virtual Environment (Strongly Recommended)

Using a virtual environment prevents dependency conflicts and ensures reproducibility.

```bash
python -m venv venv
```

Activate it:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
venv\Scripts\Activate.ps1
```

You should now see `(venv)` in your terminal prompt.

---

### 3. Install Dependencies

Install required dependencies using pip:

```bash
pip install -r requirements.txt
```

This installs all SDK runtime dependencies.

---

### 4. Install PRAXIS SDK in Editable Mode

```bash
pip install -e .
```

Installing in **editable mode** means:

* the `praxis` package becomes importable
* local code changes apply immediately
* no reinstall is required after edits

This is the **recommended setup** for development and early adopters.

## API Key Setup Documentation

### Overview
This section documents the API key authentication requirements for PRAXIS.

### Key Points
- PRAXIS implements **API key–based authentication**
- An API key is **required** for all requests
- API keys are obtained from the **PRAXIS Utility Dashboard**

### Getting Your API Key
Visit the PRAXIS Utility Dashboard to generate and manage your API keys:
- **Dashboard URL**: https://dashboard.prraas.tech

### Usage
Include your API key in request headers or query parameters as specified in the authentication guide.

### Security
- Keep your API keys confidential
- Regenerate keys if compromised
- Use environment variables to store keys securely
---

## 🔐 API Key Setup

PRAXIS uses **API key–based authentication**.

An API key is required for **all** requests.

API keys are issued from the **PRAXIS Utility Dashboard**.

---

### Option 1: Environment Variable (Recommended)

Using environment variables is the safest and cleanest approach.

**macOS / Linux**

```bash
export PRAXIS_API_KEY=your-api-key
```

**Windows (PowerShell)**

```powershell
setx PRAXIS_API_KEY "your-api-key"
```

Restart the terminal after setting the variable.

---

### Option 2: Pass API Key Explicitly

```python
from praxis import Client

client = Client(api_key="your-api-key")
```

This approach is useful for:

* quick testing
* isolated scripts
* temporary environments

For production systems, environment variables are recommended.

---

## 🌐 Base URL Configuration (Optional)

By default, the SDK connects to the **PRAXIS production API**.

If you are running a **local or self-hosted backend**, specify the base URL:

```python
client = Client(
    api_key="your-api-key",
    base_url="http://localhost:8000"
)
```

This is useful for:

* local development
* internal testing
* staging environments

---

## ✅ Verify Installation

Run the following snippet to confirm the SDK is installed correctly:

```python
from praxis import Client

client = Client()

res = client.physics.force(mass=2, acceleration=3)

print(res.data)
print(res.cost)
print(res.request_id)
```

Expected outcome:

* no import errors
* a structured response object
* valid `data`, `cost`, and `request_id`

---

## 🧪 Demo vs Production API Keys

PRAXIS may provide **demo API keys** for testing and experimentation.

* **Demo keys**

  * limited balance
  * rate-limited
  * intended for development

* **Production keys**

  * real billing
  * higher limits
  * intended for live systems

The SDK behavior is identical for both.
All enforcement happens on the backend.

---

## 🚨 Common Issues

### ❌ Missing API Key

If no API key is found, client initialization will fail.

Ensure **one** of the following:

* `PRAXIS_API_KEY` environment variable is set
* `api_key` is passed directly to `Client`

---

### ❌ Python Version Errors

If installation fails:

* verify Python ≥ 3.10
* ensure the virtual environment is activated
* upgrade pip if needed

---