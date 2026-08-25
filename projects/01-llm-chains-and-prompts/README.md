# 01 - LLM Chains & Prompt Engineering

A practical implementation of **LangChain Expression Language (LCEL)**, prompt templating, parameterized inputs, and local/cloud LLM model orchestration.

---

## 📌 Project Overview

This project demonstrates the core foundational building block of LLM applications: composing declarative pipelines using LangChain Expression Language (LCEL). It covers:
- **Text Summarization**: Structured prompt templating with parameterized variable inputs to distill documents and extract key takeaways.
- **Provider Switching**: Seamlessly running chains against local Ollama models (`gemma4:e2b`) or cloud LLMs (OpenAI, Groq).

---

## 🧠 Agentic AI Concepts Demonstrated

- **LangChain Expression Language (LCEL)**: Declarative chaining using the pipe operator (`prompt | model`).
- **Prompt Templating**: Dynamic parameter substitution using `PromptTemplate`.
- **Output Handling**: Clean AIMessage extraction and content parsing.
- **Provider Agnosticism**: Unified configuration across local open-weights models and hosted APIs.

---

## 🏗️ Architecture & Data Flow

```text
User Input (Text Article / Document)
         │
         ▼
┌─────────────────────────┐
│     PromptTemplate      │  <-- Injects text into structured prompt template
└───────────┬─────────────┘
            │ Formatted Prompt
            ▼
┌─────────────────────────┐
│  LLM (Ollama / OpenAI)  │  <-- Model generation with temperature tuning
└───────────┬─────────────┘
            │ Raw Response / AIMessage
            ▼
┌─────────────────────────┐
│     Response Output     │  <-- Clean string extraction & key findings
└─────────────────────────┘
```

---

## 🚀 Setup & Execution

### 1. Prerequisites
- Python 3.11+
- Optional: Local [Ollama](https://ollama.com/) running `gemma4:e2b` (or an `OPENAI_API_KEY` configured in `.env`).

### 2. Install Dependencies
```bash
# From repository root or project folder
pip install -e .
```

### 3. Run the CLI

**From the Repository Root:**
```bash
# Windows PowerShell
$env:PYTHONPATH = "."
uv run python .\projects\01-llm-chains-and-prompts\src\app.py

# macOS / Linux
PYTHONPATH=. uv run python projects/01-llm-chains-and-prompts/src/app.py
```

**From the Project Directory (`projects/01-llm-chains-and-prompts`):**
```bash
# Windows PowerShell
$env:PYTHONPATH = "..\..;."
uv run python src/app.py

# macOS / Linux
PYTHONPATH=../..:. uv run python src/app.py
```

**Optional Flags & Arguments:**
```bash
# Run with OpenAI
uv run python src/app.py --provider openai --model gpt-4o-mini

# Run with custom text
uv run python src/app.py --text "Agentic AI refers to autonomous systems where LLMs reason, plan, and invoke external tools dynamically."
```

### 4. Run Unit Tests
```bash
uv run pytest tests/
```

---

## 📂 Project Structure

```text
01-llm-chains-and-prompts/
├── README.md               # Project documentation
├── pyproject.toml          # Project dependencies
├── src/
│   ├── __init__.py
│   ├── summarizer.py       # LCEL summarization chain
│   └── app.py              # CLI entry point
└── tests/
    └── test_chains.py      # Unit tests with mocked LLMs
```
