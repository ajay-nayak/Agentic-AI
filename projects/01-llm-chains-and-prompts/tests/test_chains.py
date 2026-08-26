"""Unit tests for Project 01: LLM Chains and Prompts."""

import sys
from pathlib import Path
from langchain_core.language_models.fake_chat_models import FakeListChatModel
import pytest

PROJECT_SRC = Path(__file__).resolve().parent.parent / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from summarizer import (  # noqa: E402
    summarize_text,
    extract_facts,
    create_summarization_chain,
    create_facts_extraction_chain,
)


def test_summarization_chain_structure():
    fake_llm = FakeListChatModel(responses=["Mocked summary overview."])
    chain = create_summarization_chain(llm=fake_llm, mode="summary")
    assert chain is not None
    
    result = summarize_text("Some input text", llm=fake_llm, mode="summary")
    assert "Mocked summary overview." in result


def test_facts_extraction_chain():
    fake_llm = FakeListChatModel(responses=["1. Fact A\n2. Fact B"])
    chain = create_facts_extraction_chain(llm=fake_llm)
    assert chain is not None
    
    facts = extract_facts("Some detailed article", llm=fake_llm)
    assert "Fact A" in facts
    assert "Fact B" in facts
