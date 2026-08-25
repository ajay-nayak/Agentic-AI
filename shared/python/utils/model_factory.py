"""Unified LLM Model Factory supporting Ollama, OpenAI, and Groq."""

import os
from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from .logger import get_logger

logger = get_logger(__name__)


def get_chat_model(
    provider: str = "ollama",
    model_name: str | None = None,
    temperature: float = 0.2,
    **kwargs: Any
) -> BaseChatModel:
    """
    Instantiates and returns a LangChain chat model based on provider and name.
    
    Args:
        provider: One of 'ollama', 'openai', 'groq'
        model_name: Name of model (e.g. 'gemma4:e2b', 'gpt-4o-mini', 'llama-3.3-70b-versatile')
        temperature: Temperature value between 0.0 and 1.0
        **kwargs: Additional parameters passed to the chat model constructor
        
    Returns:
        BaseChatModel: LangChain compatible chat model instance
    """
    provider_lower = provider.lower().strip()
    
    if provider_lower == "ollama":
        try:
            from langchain_ollama import ChatOllama
            selected_model = model_name or "gemma4:e2b"
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            logger.info(f"Initializing ChatOllama model: '{selected_model}' at {base_url}")
            return ChatOllama(model=selected_model, temperature=temperature, base_url=base_url, **kwargs)
        except ImportError:
            raise ImportError("langchain-ollama is required. Run 'pip install langchain-ollama'")
            
    elif provider_lower == "openai":
        try:
            from langchain_openai import ChatOpenAI
            selected_model = model_name or "gpt-4o-mini"
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.warning("OPENAI_API_KEY is not set in environment variables.")
            logger.info(f"Initializing ChatOpenAI model: '{selected_model}'")
            return ChatOpenAI(model=selected_model, temperature=temperature, **kwargs)
        except ImportError:
            raise ImportError("langchain-openai is required. Run 'pip install langchain-openai'")
            
    elif provider_lower == "groq":
        try:
            from langchain_groq import ChatGroq
            selected_model = model_name or "llama-3.3-70b-versatile"
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                logger.warning("GROQ_API_KEY is not set in environment variables.")
            logger.info(f"Initializing ChatGroq model: '{selected_model}'")
            return ChatGroq(model_name=selected_model, temperature=temperature, **kwargs)
        except ImportError:
            raise ImportError("langchain-groq is required. Run 'pip install langchain-groq'")
            
    else:
        raise ValueError(f"Unsupported LLM provider: '{provider}'. Supported: 'ollama', 'openai', 'groq'")
