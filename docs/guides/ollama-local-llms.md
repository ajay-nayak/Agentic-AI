# Ollama Local LLMs Setup & Execution Guide

Running local language models allows you to develop, test, and experiment with Agentic AI pipelines completely offline with zero API costs and full data privacy.

---

## 1. Installation

1. Download and install Ollama from [ollama.com](https://ollama.com/).
2. Verify installation:
```bash
ollama --version
```

---

## 2. Recommended Models for this Repository

| Model | Size | Best For | Pull Command |
| :--- | :--- | :--- | :--- |
| `gemma4:e2b` / `gemma2:2b` | ~1.6 GB | Fast local agent routing, chains | `ollama pull gemma2:2b` |
| `gemma3:1b` / `gemma3:270m` | ~300 MB - 1 GB | Ultra-lightweight prompt experimentation | `ollama pull gemma3:1b` |
| `llama3.2:3b` | ~2.0 GB | High-accuracy local tool calling | `ollama pull llama3.2:3b` |

---

## 3. Automated Model Puller

You can run the repository's helper script to pull all recommended models:

```bash
python scripts/setup/pull_ollama_models.py
```

---

## 4. Serving & Custom Port Configuration

By default, Ollama listens on `http://localhost:11434`. If running on a remote machine or custom port, set the `OLLAMA_BASE_URL` in your `.env` file:

```env
OLLAMA_BASE_URL=http://localhost:11434
```
