# React & Frontend Integration Architecture

This guide explains how modern React and web client frontends interface with Agentic AI backends, LangGraph workflows, and streaming LLM pipelines.

---

## 1. Full-Stack Agentic Architecture

```mermaid
graph LR
    subgraph Client["React Client (Next.js / Vite)"]
        UI[Chat / Workflow UI]
        Hook[useChat / useStream]
        Store[State Store (Zustand/Redux)]
    end

    subgraph Gateway["Backend Gateway (FastAPI / Express)"]
        API[Streaming SSE / WebSocket Endpoint]
        Auth[Auth & Rate Limiting]
    end

    subgraph AgentEngine["Agent Engine"]
        Graph[LangGraph StateGraph]
        Checkpointer[(Postgres / SQLite Checkpoints)]
        Tools[External Tools & Tavily API]
    end

    UI --> Hook
    Hook --> Store
    Hook <==>|Server-Sent Events (SSE)| API
    API --> Graph
    Graph --> Checkpointer
    Graph --> Tools
```

---

## 2. Key Frontend Integration Concepts

### A. Real-Time Streaming (Server-Sent Events)
Agentic systems produce multiple event types during execution:
1. **Token Events**: Partial string chunks for real-time text rendering.
2. **Tool Execution Events**: `tool_start`, `tool_input`, `tool_end` showing users what tool the agent is invoking.
3. **Graph State Updates**: Node transitions notifying the UI which node in the graph is currently active.

```typescript
// Example React EventSource listener
const eventSource = new EventSource(`/api/agent/stream?query=${encodeURIComponent(query)}`);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === "token") {
    appendToken(data.content);
  } else if (data.type === "tool_call") {
    showToolIndicator(data.tool_name, data.args);
  } else if (data.type === "complete") {
    finishGeneration();
  }
};
```

---

## 3. Human-in-the-Loop (HITL) Approvals in React

When an agent executes high-impact actions (e.g., executing code, placing orders, deleting records), the graph pauses execution using LangGraph `interrupt()`:

1. **Backend Pause**: The backend yields an `interrupt_required` event with action payload and thread ID.
2. **Frontend Modal**: React renders an interactive confirmation modal with "Approve", "Modify", or "Reject" buttons.
3. **Resume Execution**: On approval, React sends a `POST /api/agent/resume` with `{ thread_id, approved: true }`.
