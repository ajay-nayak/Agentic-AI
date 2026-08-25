# 01 - LLM Chains & Prompt Engineering

A practical implementation of **LangChain Expression Language (LCEL)**, prompt templating, few-shot prompting, and local/cloud LLM model orchestration.

---

## 📌 Project Overview

This project demonstrates the core foundational building block of LLM applications: composing declarative pipelines using LangChain Expression Language (LCEL). It covers:
1. **Text Summarization**: Structured prompt templating with parameterized variable inputs to distill documents and extract key takeaways.
2. **Few-Shot Guided Generation**: Constrained, few-shot guided prompt engineering for deterministic password generation with anchored character sets.

---

## 🧠 Agentic AI Concepts Demonstrated

- **LangChain Expression Language (LCEL)**: Declarative chaining using the pipe operator (`prompt | model`).
- **Prompt Templating**: Dynamic parameter substitution using `PromptTemplate`.
- **Few-Shot Prompting**: Providing pattern demonstrations inside the context to steer model entropy and format.
- **Provider Agnosticism**: Seamlessly switching between local Ollama instances (`gemma4:e2b`, `gemma3:1b`) and cloud providers (OpenAI, Groq).

---

## 🏗️ Architecture & Data Flow

```text
User Input (Text / Seed)
         │
         ▼
┌─────────────────────────┐
│     PromptTemplate      │  <-- Injects variables into structured prompt
└───────────┬─────────────┘
            │ Formatted Prompt
            ▼
┌─────────────────────────┐
│  LLM (Ollama / OpenAI)  │  <-- Model generation with temperature tuning
└───────────┬─────────────┘
            │ Raw Response / AIMessage
            ▼
┌─────────────────────────┐
│     Response Output     │  <-- Clean string extraction
└─────────────────────────┘
```

---

## 🚀 Setup & Execution

### 1. Prerequisites
- Python 3.11+
- Optional: Local [Ollama](https://ollama.com/) running `gemma4:e2b` or `gemma3:1b` (or an `OPENAI_API_KEY` configured in `.env`).

### 2. Install Dependencies
```bash
# From repository root or project folder
pip install -e .
```

### 3. Run the CLI
```bash
# Run both summarizer and password generator using Ollama (default)
python -m src.app

# Run with OpenAI
python -m src.app --provider openai --model gpt-4o-mini

# Run specific task
python -m src.app --task summarize
```

### 4. Run Unit Tests
```bash
pytest tests/
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
│   ├── password_generator.py # Few-shot password generator
│   └── app.py              # CLI entry point
└── tests/
    └── test_chains.py      # Unit tests with mocked LLMs
```
