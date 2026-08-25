# 02 - Model Switching & Multi-Model Benchmarking (Groq)

A clean implementation demonstrating **multi-model orchestration, dynamic LLM provider switching, and performance/quality benchmarking** using Groq's high-speed inference engine.

---

## 📌 Project Overview

In agentic architectures, different tasks require different model profiles:
- **Instant / High Throughput Models** (e.g., `llama-4-8b-instant`, `llama-3.1-8b-instant`) are ideal for sub-second tool routing, classification, and JSON extraction.
- **High Parameter Versatile Models** (e.g., `llama-3.3-70b-versatile`) are suited for complex reasoning, multi-step planning, and nuanced code generation.

This project encapsulates a structured `GroqModelSwitcher` that allows applications to dynamically choose models based on latency and capability requirements, complete with mock fallbacks for offline testing.

---

## 🧠 Agentic AI Concepts Demonstrated

- **Dynamic Model Selection**: Switching inference backends on the fly based on task difficulty.
- **Provider Routing**: Managing API authentication, temperature controls, and parameter variations across model families.
- **Multi-Model Comparison**: Fan-out querying to compare answers from multiple LLMs simultaneously.
- **Resilient Fallback Mode**: Graceful offline simulation for continuous testing environments.

---

## 🏗️ Architecture

```text
Query Prompt
     │
     ▼
┌───────────────────────────────┐
│      GroqModelSwitcher        │
└──────────────┬────────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌──────────────┐  ┌──────────────┐
│   Llama 4    │  │  Llama 3.3   │
│ (Low Latency)│  │ (Reasoning)  │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                ▼
      ┌──────────────────┐
      │ Benchmark Output │
      └──────────────────┘
```

---

## 🚀 Setup & Execution

### 1. Prerequisites
- Python 3.11+
- Optional: `GROQ_API_KEY` set in your `.env` file (get a free key at [console.groq.com](https://console.groq.com/keys)).

### 2. Install Dependencies
```bash
pip install -e .
```

### 3. Run the CLI

**From the Repository Root:**
```bash
# Windows PowerShell
$env:PYTHONPATH = "."
uv run python .\projects\02-model-switching-groq\src\app.py

# macOS / Linux
PYTHONPATH=. uv run python projects/02-model-switching-groq/src/app.py
```

**From the Project Directory (`projects/02-model-switching-groq`):**
```bash
# Windows PowerShell
$env:PYTHONPATH = "..\..;."
uv run python src/app.py

# macOS / Linux
PYTHONPATH=../..:. uv run python src/app.py
```

**Optional Flags & Arguments:**
```bash
# Force offline mock execution
uv run python src/app.py --mock

# Query with custom prompt
uv run python src/app.py --prompt "Explain the difference between deterministic and agentic AI."
```

### 4. Run Unit Tests
```bash
uv run pytest tests/
```

---

## 📂 Project Structure

```text
02-model-switching-groq/
├── README.md               # Project documentation
├── pyproject.toml          # Dependencies
├── src/
│   ├── __init__.py
│   ├── model_switcher.py   # Model switcher & comparison logic
│   └── app.py              # CLI runner
└── tests/
    └── test_model_switcher.py # Unit tests
```
