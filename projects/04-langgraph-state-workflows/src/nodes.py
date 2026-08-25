"""Node functions representing individual steps in the LangGraph workflow."""

from shared.python.utils.logger import get_logger
try:
    from .state import ResearchState
except (ImportError, ValueError):
    from state import ResearchState

logger = get_logger(__name__)


def classify_intent_node(state: ResearchState) -> dict:
    """Classifies query complexity to determine whether deep research is required."""
    query = state["query"].lower()
    complex_triggers = ["compare", "difference", "research", "architecture", "deep", "analyze", "jobs"]
    is_complex = any(trigger in query for trigger in complex_triggers)
    
    logger.info(f"Node [classify_intent]: is_complex = {is_complex}")
    return {
        "is_complex": is_complex,
        "iteration_count": state.get("iteration_count", 0) + 1
    }


def research_node(state: ResearchState) -> dict:
    """Simulates or performs external research retrieval, appending findings to state."""
    query = state["query"]
    logger.info(f"Node [research]: Conducting research for '{query}'")
    
    findings = [
        "Key Fact A: Agentic AI systems employ autonomous decision loops (Plan -> Act -> Observe).",
        "Key Fact B: LangGraph introduces cyclic graph topologies with state persistence and human-in-the-loop control."
    ]
    return {
        "research_notes": findings,
        "iteration_count": state.get("iteration_count", 0) + 1
    }


def direct_answer_node(state: ResearchState) -> dict:
    """Generates an immediate concise answer for simple queries."""
    query = state["query"]
    logger.info(f"Node [direct_answer]: Answering simple query '{query}'")
    
    return {
        "final_answer": f"Direct response: The query '{query}' is straightforward and resolved without deep research."
    }


def synthesize_node(state: ResearchState) -> dict:
    """Synthesizes researched context into a comprehensive structured answer."""
    query = state["query"]
    notes = state.get("research_notes", [])
    logger.info(f"Node [synthesize]: Synthesizing {len(notes)} notes for '{query}'")
    
    notes_formatted = "\n".join(f"- {note}" for note in notes)
    final_output = (
        f"Comprehensive Analysis for '{query}':\n\n"
        f"Synthesized Findings:\n{notes_formatted}\n\n"
        f"Conclusion: Successfully orchestrated via LangGraph multi-node state graph."
    )
    return {
        "final_answer": final_output
    }
