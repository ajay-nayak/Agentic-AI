"""State definition and reducers for LangGraph agent workflow."""

from typing import TypedDict, List, Annotated
import operator


class ResearchState(TypedDict):
    """
    Typed dictionary representing the shared state across graph nodes.
    
    Attributes:
        query: The initial user prompt.
        is_complex: Flag determined by classifier node indicating if research step is needed.
        research_notes: Annotated list of notes accumulated via operator.add reducer.
        final_answer: Synthesized final output.
        iteration_count: Current step counter to enforce loop bounds.
    """
    query: str
    is_complex: bool
    research_notes: Annotated[List[str], operator.add]
    final_answer: str
    iteration_count: int
