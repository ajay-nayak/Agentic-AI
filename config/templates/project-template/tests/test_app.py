"""Unit tests for template project."""

import sys
from pathlib import Path

PROJECT_SRC = Path(__file__).resolve().parent.parent / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from app import sample_function  # noqa: E402


def test_sample_function():
    assert sample_function() == "Hello from template agent!"
