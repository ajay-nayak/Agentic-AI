# LangGraph State Workflows & Cyclic Graph Orchestration

This document covers the architectural principles of **LangGraph**, the framework for building stateful, multi-actor applications with LLMs.

---

## 1. Why LangGraph?

While LCEL is suited for linear Directed Acyclic Graphs (DAGs), agentic workflows require:
- **Cycles**: Looping through reasoning, tool execution, and self-reflection until a satisfaction condition is met.
- **State Management**: Passing shared, mutable, or append-only state structures across discrete nodes.
- **Persistence & Time-Travel**: Checkpointing state to disk or database to inspect intermediate states or resume paused runs.
- **Multi-Agent Coordination**: Managing supervisor, hierarchical, or peer-to-peer agent collaborations.

---

## 2. Core Building Blocks

### A. State Schema
The single source of truth passed across all nodes in the graph. Defined via `TypedDict` or `Pydantic`:

```python
from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    next_step: str
```

### B. Nodes
Python functions that accept the current `State` and return a dictionary of state updates:

```python
def analyze_node(state: AgentState) -> dict:
    return {"next_step": "execute"}
```

### C. Edges
- **Normal Edges**: Direct transitions (`builder.add_edge("node_a", "node_b")`).
- **Conditional Edges**: Dynamic routing based on a router function (`builder.add_conditional_edges("router_node", condition_fn, mapping)`).

---

## 3. Human-in-the-Loop & Interrupts

LangGraph supports pausing graph execution prior to executing critical nodes:

```python
# Compiling graph with checkpoint persistence
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = builder.compile(checkpointer=memory, interrupt_before=["execute_action_node"])
```
