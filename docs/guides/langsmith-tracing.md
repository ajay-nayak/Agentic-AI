# LangSmith Observability & Tracing Guide

**LangSmith** provides full observability into complex agentic loops, prompt latency, token costs, and tool execution traces.

---

## 1. Setup & Account Configuration

1. Create a free account at [smith.langchain.com](https://smith.langchain.com/).
2. Navigate to **Settings** -> **API Keys** and generate a new key.

---

## 2. Environment Variable Configuration

Add the following lines to your root `.env` file:

```env
# Enable automatic tracing
LANGSMITH_TRACING=true

# API Endpoint (Default US endpoint)
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# For European Union accounts, use:
# LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com

# Your LangSmith API Key
LANGSMITH_API_KEY=your_langsmith_api_key_here

# Project Name under which traces will be organized
LANGSMITH_PROJECT=agentic-ai-portfolio
```

---

## 3. What You Can Inspect in LangSmith

Once enabled, LangChain and LangGraph automatically stream every run to your dashboard:
- **Full Trace Tree**: Step-by-step breakdown of prompt inputs, LLM outputs, tool calls, and state transitions.
- **Latency Analysis**: Exact time spent in model reasoning vs. external tool network calls.
- **Token Usage**: Input/output token metrics across multi-agent loops.
- **Error Diagnostics**: Complete stack traces and raw model responses during failures.
