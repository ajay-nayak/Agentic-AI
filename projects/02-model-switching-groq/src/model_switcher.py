"""Groq model switching, validation, and multi-model benchmarking."""

import os
from typing import Dict, List, Any
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from shared.python.utils.logger import get_logger
from shared.python.utils.env_loader import load_project_env

load_project_env()
logger = get_logger(__name__)

VALID_GROQ_MODELS = [
    "llama-4-8b-instant",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]


class MockAIMessage:
    """Simulated AI message container."""
    def __init__(self, content: str):
        self.content = content


class MockChatGroq:
    """Mock ChatGroq class for testing and offline educational execution."""
    def __init__(self, model_name: str, temperature: float = 0.0, max_retries: int = 2):
        if model_name not in VALID_GROQ_MODELS:
            raise ValueError(f"Invalid model: '{model_name}'. Valid models: {VALID_GROQ_MODELS}")
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries
        
    def invoke(self, messages: List[Any]) -> MockAIMessage:
        if not messages or not isinstance(messages, list):
            raise ValueError("Messages must be a non-empty list")
            
        if self.model_name == "llama-4-8b-instant":
            content = "[Llama 4] Machine learning enables algorithms to learn patterns and make predictions directly from data."
        elif self.model_name == "llama-3.3-70b-versatile":
            if self.temperature > 0.2:
                content = "[Llama 3.3 Creative] Machine learning is akin to teaching software through experience and patterns rather than static rules!"
            else:
                content = "[Llama 3.3] Machine learning is a branch of artificial intelligence focused on building applications that learn from data."
        else:
            content = f"[Mock {self.model_name}] Simulated response for given prompt."
            
        return MockAIMessage(content)


class GroqModelSwitcher:
    """Manages switching and querying across different Groq LLM model endpoints."""
    
    def __init__(self, use_mock: bool = False, api_key: str | None = None):
        self.use_mock = use_mock
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
            
        if not self.use_mock and "GROQ_API_KEY" not in os.environ:
            logger.warning("GROQ_API_KEY not found. Defaulting to mock execution mode.")
            self.use_mock = True

    def get_model(self, model_name: str, temperature: float = 0.0) -> Any:
        """Instantiates a model instance."""
        if model_name not in VALID_GROQ_MODELS:
            raise ValueError(f"Unknown model '{model_name}'. Valid options: {VALID_GROQ_MODELS}")
            
        if self.use_mock:
            return MockChatGroq(model_name=model_name, temperature=temperature)
            
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(model_name=model_name, temperature=temperature)
        except Exception as e:
            logger.warning(f"Failed to initialize real ChatGroq: {e}. Falling back to mock.")
            return MockChatGroq(model_name=model_name, temperature=temperature)

    def query(self, model_name: str, prompt: str, temperature: float = 0.0) -> str:
        """Queries a specific model with a text prompt."""
        model = self.get_model(model_name, temperature=temperature)
        messages = [HumanMessage(content=prompt)] if not isinstance(model, MockChatGroq) else [{"role": "user", "content": prompt}]
        response = model.invoke(messages)
        if hasattr(response, "content"):
            return str(response.content)
        return str(response)


def compare_models(prompt: str, models: List[str] | None = None, use_mock: bool = False) -> Dict[str, str]:
    """Queries multiple models with the same prompt to compare speed and response quality."""
    target_models = models or ["llama-4-8b-instant", "llama-3.3-70b-versatile"]
    switcher = GroqModelSwitcher(use_mock=use_mock)
    results = {}
    
    for model_name in target_models:
        try:
            temp = 0.7 if "versatile" in model_name else 0.0
            results[model_name] = switcher.query(model_name, prompt, temperature=temp)
        except Exception as e:
            results[model_name] = f"Error querying {model_name}: {e}"
            
    return results
