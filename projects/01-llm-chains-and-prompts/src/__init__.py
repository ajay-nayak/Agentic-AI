"""Chains and Prompts package."""

from .summarizer import (
    summarize_text,
    extract_facts,
    create_summarization_chain,
    create_facts_extraction_chain,
)

__all__ = [
    "summarize_text",
    "extract_facts",
    "create_summarization_chain",
    "create_facts_extraction_chain",
]
