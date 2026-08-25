# Environment Setup Guide

This guide covers setting up Python environments, dependency management with `uv` or `pip`, and configuring API keys across the repository.

---

## 1. Prerequisites
- **Python 3.11+** installed and available in PATH.
- **Git** installed.
- Optional: **Ollama** for running local models.

---

## 2. Setting Up with `uv` (Recommended)

`uv` is an extremely fast Python package and project manager.

```bash
# 1. Install uv (if not installed)
pip install uv

# 2. Create and activate a virtual environment
uv venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# 3. Install repository workspace in editable mode with dev dependencies
uv pip install -e ".[dev]"
```

---

## 3. Setting Up with Standard `pip`

```bash
python -m venv .venv
# Activate
.venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

---

## 4. Environment Variables Configuration

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Populate the required credentials in `.env`:
- `OPENAI_API_KEY`: For OpenAI models.
- `GROQ_API_KEY`: For Groq fast inference models.
- `TAVILY_API_KEY`: For Tavily web search agent.
- `LANGSMITH_API_KEY`: For tracing and observability.

---

## 5. Automated Setup Check

Run the automated setup utility to verify your environment:

```bash
python scripts/setup/setup_env.py
```
