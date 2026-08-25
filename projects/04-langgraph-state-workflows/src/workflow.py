"""LangGraph StateGraph construction, conditional routing, and compilation."""

from typing import Any, Dict
from langgraph.graph import StateGraph, START, END
from shared.python.utils.logger import get_logger

try:
    from .state import ResearchState
    from .nodes import classify_intent_node, research_node, direct_answer_node, synthesize_node
except (ImportError, ValueError):
    from state import ResearchState
    from nodes import classify_intent_node, research_node, direct_answer_node, synthesize_node

logger = get_logger(__name__)


def route_by_complexity(state: ResearchState) -> str:
    """Conditional edge routing logic."""
    if state.get("is_complex", False):
        return "research_node"
    return "direct_answer_node"


def build_research_graph() -> Any:
    """
    Constructs and compiles the StateGraph.
    
    Graph Topology:
        START -> classify_intent
                    │
            ┌───────┴────────┐
        (complex)        (simple)
            ▼                ▼
      research_node   direct_answer_node
            │                │
            ▼                ▼
      synthesize_node       END
            │
            ▼
           END
    """
    builder = StateGraph(ResearchState)
    
    # 1. Add Nodes
    builder.add_node("classify_intent", classify_intent_node)
    builder.add_node("research_node", research_node)
    builder.add_node("direct_answer_node", direct_answer_node)
    builder.add_node("synthesize_node", synthesize_node)
    
    # 2. Add Edges & Conditional Routing
    builder.add_edge(START, "classify_intent")
    builder.add_conditional_edges(
        "classify_intent",
        route_by_complexity,
        {
            "research_node": "research_node",
            "direct_answer_node": "direct_answer_node"
        }
    )
    builder.add_edge("research_node", "synthesize_node")
    builder.add_edge("synthesize_node", END)
    builder.add_edge("direct_answer_node", END)
    
    # 3. Compile
    return builder.compile()


def run_research_workflow(query: str) -> Dict[str, Any]:
    """Executes the workflow graph for a given user query."""
    graph = build_research_graph()
    initial_state: ResearchState = {
        "query": query,
        "is_complex": False,
        "research_notes": [],
        "final_answer": "",
        "iteration_count": 0
    }
    logger.info(f"Executing LangGraph workflow for query: '{query}'")
    final_state = graph.invoke(initial_state)
    return final_state
