# 03 - Autonomous AI Search Agent (ReAct + Tool Calling)

An autonomous **ReAct (Reasoning + Acting) Agent** built with LangChain, tool calling, Tavily web search integration, and multi-model backend execution (local Ollama, OpenAI, or Groq).

---

## 📌 Project Overview

Unlike static prompt chains that execute pre-defined sequences, an **Agent** acts as a dynamic decision engine. Given a goal, the LLM determines:
1. Does it need external data?
2. Which tool should it invoke and with what parameters?
3. How to evaluate the tool output (Observation) and decide whether further research is required or the final response can be formulated.

This project implements an autonomous web search agent that interfaces with the Tavily Search API and supports offline simulated fallbacks.

---

## 🧠 Agentic AI Concepts Demonstrated

- **Agent Reasoning Loop (ReAct)**: Alternating between Thought, Action (Tool Execution), and Observation.
- **Dynamic Tool Calling**: Equipping the model with `@tool` definitions and allowing the LLM to trigger schema-validated arguments.
- **External API Grounding**: Live search integration with Tavily to eliminate hallucinations on recent/temporal facts.
- **Resilient Tool Design**: Graceful fallback to offline mock search when external API credentials are not provided.

---

## 🏗️ Architecture & ReAct Cycle

```text
User Query: "Find senior AI developer jobs in Bangalore"
                           │
                           ▼
              ┌───────────────────────────┐
              │     LLM Reasoning Engine   │
              │  (Ollama / OpenAI / Groq)  │
              └─────────────┬─────────────┘
                            │
               ┌────────────┴────────────┐
       [Needs Web Info]             [Has Direct Answer]
               ▼                             ▼
   ┌───────────────────────┐         ┌────────────────┐
   │ Tool Call: search()   │         │ Final Response │
   └───────────┬───────────┘         └────────────────┘
               │
               ▼
   ┌───────────────────────┐
   │ Tavily Search API     │
   └───────────┬───────────┘
               │
               ▼ Observation (Search Results)
   ┌───────────────────────┐
   │   State Update Loop   │ ───► (Synthesizes & Returns Final Answer)
   └───────────────────────┘
```

---

## 🚀 Setup & Execution

### 1. Prerequisites
- Python 3.11+
- Optional: `TAVILY_API_KEY` in `.env` (get a free API key at [tavily.com](https://tavily.com)).
- Optional: Local Ollama instance running `gemma4:e2b` or an `OPENAI_API_KEY`.

### 2. Install Dependencies
```bash
pip install -e .
```

### 3. Run the Search Agent

**From the Repository Root:**
```bash
# Windows PowerShell
$env:PYTHONPATH = "."
uv run python .\projects\03-ai-search-agent\src\app.py

# macOS / Linux
PYTHONPATH=. uv run python projects/03-ai-search-agent/src/app.py
```

**From the Project Directory (`projects/03-ai-search-agent`):**
```bash
# Windows PowerShell
$env:PYTHONPATH = "..\..;."
uv run python src/app.py

# macOS / Linux
PYTHONPATH=../..:. uv run python src/app.py
```

**Optional Flags & Arguments:**
```bash
# Run with custom query
uv run python src/app.py --query "What are the latest developments in AI Agent memory systems in 2026?"

# Run with OpenAI GPT-4o-mini
uv run python src/app.py --provider openai --model gpt-4o-mini
```

### 4. Run Unit Tests
```bash
uv run pytest tests/
```

---

## 📂 Project Structure

```text
03-ai-search-agent/
├── README.md           # Project documentation
├── pyproject.toml      # Dependencies
├── src/
│   ├── __init__.py
│   ├── tools.py        # Tavily search tool + offline fallback
│   ├── agent.py        # ReAct agent builder & invocation
│   └── app.py          # CLI runner
└── tests/
    └── test_agent.py   # Unit tests
```
