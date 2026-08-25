"""Unit tests for Project 03: AI Search Agent."""

import sys
from pathlib import Path
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
import pytest

PROJECT_SRC = Path(__file__).resolve().parent.parent / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from tools import create_search_tool  # noqa: E402
from agent import run_search_agent  # noqa: E402


def test_search_tool_execution():
    search_tool = create_search_tool()
    result = search_tool.invoke("Bangalore senior mobile developer jobs")
    assert result is not None
    assert len(str(result)) > 10


def test_run_search_agent_with_mock():
    mock_agent = MagicMock()
    mock_agent.invoke.return_value = {
        "messages": [AIMessage(content="Here are 3 mobile AI jobs in Bangalore...")]
    }
    
    result = run_search_agent("Find AI jobs", agent=mock_agent)
    assert "messages" in result
    assert mock_agent.invoke.called
