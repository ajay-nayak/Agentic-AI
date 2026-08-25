"""Unit tests for Project 01: LLM Chains and Prompts."""

import sys
from pathlib import Path
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
from langchain_core.language_models.fake_chat_models import FakeListChatModel
import pytest

PROJECT_SRC = Path(__file__).resolve().parent.parent / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from summarizer import summarize_text, create_summarization_chain  # noqa: E402
from password_generator import generate_password, create_password_chain  # noqa: E402


def test_summarization_chain_structure():
    fake_llm = FakeListChatModel(responses=["Mocked summary with 2 findings."])
    chain = create_summarization_chain(llm=fake_llm)
    assert chain is not None
    
    result = summarize_text("Some input text", llm=fake_llm)
    assert "Mocked summary with 2 findings." in result


def test_password_generation_chain():
    fake_llm = FakeListChatModel(responses=["P@ss1\nP@ss2\nP@ss3"])
    chain = create_password_chain(llm=fake_llm, use_few_shot=True)
    assert chain is not None
    
    passwords = generate_password("testseed", llm=fake_llm, use_few_shot=True)
    assert "P@ss1" in passwords
    assert len(passwords.splitlines()) == 3
