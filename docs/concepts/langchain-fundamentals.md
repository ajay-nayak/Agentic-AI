# LangChain Fundamentals & Core Concepts

This document summarizes the foundational LangChain components and design patterns utilized across projects in this repository.

---

## 1. LangChain Expression Language (LCEL)

LCEL is a declarative, composable syntax for chaining runnables together using the Unix-style pipe (`|`) operator.

### Core Runnable Protocol
Every LCEL component implements common methods:
- `invoke()`: Synchronous execution on a single input.
- `ainvoke()`: Asynchronous execution.
- `stream()`: Stream back output chunks in real time.
- `batch()`: Efficient batch execution over an iterable of inputs.

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# LCEL Pipeline: Prompt -> LLM -> Output Parser
chain = prompt | model | StrOutputParser()
result = chain.invoke({"input_variable": "value"})
```

---

## 2. Models & Providers

LangChain standardizes chat models across various inference engines:
- **Local Models**: `ChatOllama` connects to locally hosted open-weights models without network latency or API fees.
- **Cloud Models**: `ChatOpenAI`, `ChatGroq`, `ChatAnthropic` connect to hosted APIs.

---

## 3. Prompts & Output Parsers

- **PromptTemplate**: Formats parameterized inputs into clean textual prompt strings.
- **ChatPromptTemplate**: Formats role-based messages (`SystemMessage`, `HumanMessage`, `AIMessage`).
- **Structured Output Parsers**: Uses Pydantic schemas or function calling to ensure LLM outputs conform to strict JSON specifications.

---

## 4. Tools & Tool Calling

A **Tool** is a callable capability decorated with `@tool` and detailed type annotations and docstrings:

```python
from langchain_core.tools import tool

@tool
def calculate_tax(income: float, rate: float = 0.2) -> float:
    """Calculates income tax given gross income and tax rate."""
    return income * rate
```

When bound to a model (`model.bind_tools([calculate_tax])`), the model generates structured arguments for tool execution when needed.
