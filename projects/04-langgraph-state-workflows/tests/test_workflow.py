"""Unit tests for Project 04: LangGraph State Workflows."""

import sys
from pathlib import Path
import pytest

PROJECT_SRC = Path(__file__).resolve().parent.parent / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from workflow import build_research_graph, run_research_workflow  # noqa: E402


def test_build_research_graph():
    graph = build_research_graph()
    assert graph is not None


def test_complex_query_flow():
    state = run_research_workflow("Please research and analyze agent architectures.")
    assert state["is_complex"] is True
    assert len(state["research_notes"]) > 0
    assert "Comprehensive Analysis" in state["final_answer"]
    assert state["iteration_count"] >= 2


def test_simple_query_flow():
    state = run_research_workflow("Hello world")
    assert state["is_complex"] is False
    assert len(state["research_notes"]) == 0
    assert "Direct response" in state["final_answer"]
