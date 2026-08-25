"""Unit tests for Project 02: Model Switching."""

import sys
from pathlib import Path
import pytest

PROJECT_SRC = Path(__file__).resolve().parent.parent / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from model_switcher import GroqModelSwitcher, compare_models, VALID_GROQ_MODELS  # noqa: E402


def test_valid_models_list():
    assert "llama-4-8b-instant" in VALID_GROQ_MODELS
    assert "llama-3.3-70b-versatile" in VALID_GROQ_MODELS


def test_mock_query_execution():
    switcher = GroqModelSwitcher(use_mock=True)
    res = switcher.query("llama-4-8b-instant", "What is AI?")
    assert "[Llama 4]" in res


def test_invalid_model_rejection():
    switcher = GroqModelSwitcher(use_mock=True)
    with pytest.raises(ValueError):
        switcher.get_model("unsupported-model-xyz")


def test_model_comparison():
    res = compare_models("Explain recursion", models=["llama-4-8b-instant", "llama-3.3-70b-versatile"], use_mock=True)
    assert len(res) == 2
    assert "llama-4-8b-instant" in res
    assert "llama-3.3-70b-versatile" in res
