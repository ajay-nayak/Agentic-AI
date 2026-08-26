"""Text summarization and key facts extraction using LangChain Expression Language (LCEL)."""

from typing import Literal
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import RunnableSerializable

from shared.python.utils.model_factory import get_chat_model
from shared.python.utils.env_loader import load_project_env
from shared.prompts.system_prompts import (
    SUMMARIZER_ONLY_PROMPT_TEMPLATE,
    FACTS_EXTRACTION_PROMPT_TEMPLATE,
    SUMMARIZER_PROMPT_TEMPLATE,
)

load_project_env()

ModeType = Literal["summary", "facts", "full"]


def get_template_for_mode(mode: ModeType = "full") -> str:
    """Returns appropriate prompt template for requested analysis mode."""
    if mode == "summary":
        return SUMMARIZER_ONLY_PROMPT_TEMPLATE
    elif mode == "facts":
        return FACTS_EXTRACTION_PROMPT_TEMPLATE
    return SUMMARIZER_PROMPT_TEMPLATE


def create_summarization_chain(
    llm: BaseChatModel | None = None,
    mode: ModeType = "full",
) -> RunnableSerializable:
    """
    Creates an LCEL chain for text summarization or facts extraction.
    
    Args:
        llm: Optional chat model instance. Defaults to local Ollama.
        mode: One of 'summary', 'facts', or 'full'.
        
    Returns:
        RunnableSerializable: Executable LCEL chain.
    """
    model = llm or get_chat_model(provider="ollama", model_name="gemma4:e2b", temperature=0.2)
    template_str = get_template_for_mode(mode)
    prompt = PromptTemplate(input_variables=["text"], template=template_str)
    
    # LCEL Composition: PromptTemplate | ChatModel
    return prompt | model


def create_facts_extraction_chain(llm: BaseChatModel | None = None) -> RunnableSerializable:
    """Creates a dedicated LCEL chain to extract 2 interesting facts."""
    return create_summarization_chain(llm=llm, mode="facts")


def summarize_text(
    text: str,
    llm: BaseChatModel | None = None,
    mode: ModeType = "full",
) -> str:
    """
    Processes text using the LCEL pipeline for summarization or facts extraction.
    
    Args:
        text: Input text string to process.
        llm: Optional LLM model instance.
        mode: 'summary' for concise summary, 'facts' for 2 interesting facts, 'full' for both.
        
    Returns:
        str: Output response content.
    """
    chain = create_summarization_chain(llm=llm, mode=mode)
    response = chain.invoke(input={"text": text})
    if isinstance(response, BaseMessage):
        return str(response.content)
    return str(response)


def extract_facts(text: str, llm: BaseChatModel | None = None) -> str:
    """
    Dedicated helper to extract 2 interesting facts from text.
    
    Args:
        text: Input text string.
        llm: Optional LLM model instance.
        
    Returns:
        str: 2 interesting facts formatted as markdown.
    """
    return summarize_text(text, llm=llm, mode="facts")
