"""Autonomous ReAct search agent builder and executor."""

from typing import List, Any
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
from shared.python.utils.logger import get_logger
from shared.python.utils.model_factory import get_chat_model
from shared.python.utils.env_loader import load_project_env
try:
    from .tools import search, create_search_tool
except (ImportError, ValueError):
    from tools import search, create_search_tool

load_project_env()
logger = get_logger(__name__)


def create_search_agent(llm: BaseChatModel | None = None, custom_tools: List[Any] | None = None) -> Any:
    """
    Constructs an agent equipped with search tooling.
    
    Args:
        llm: Chat model instance (defaults to Ollama gemma4:e2b)
        custom_tools: List of LangChain tools (defaults to [search])
        
    Returns:
        Agent executor or runnable graph.
    """
    model = llm or get_chat_model(provider="ollama", model_name="gemma4:e2b", temperature=0.1)
    tools = custom_tools or [search]
    
    try:
        # Try LangChain 1.x create_agent or langgraph prebuilt react agent
        from langchain.agents import create_agent
        return create_agent(model=model, tools=tools)
    except Exception:
        try:
            from langgraph.prebuilt import create_react_agent
            return create_react_agent(model=model, tools=tools)
        except Exception as e:
            logger.warning(f"Could not initialize standard create_agent: {e}. Falling back to tool-bound model.")
            return model.bind_tools(tools) if hasattr(model, "bind_tools") else model


def run_search_agent(query: str, agent: Any = None, llm: BaseChatModel | None = None) -> Any:
    """
    Executes the search agent for a given query.
    
    Args:
        query: User question or search request.
        agent: Pre-initialized agent instance.
        llm: Optional LLM model instance.
        
    Returns:
        Agent output dictionary or response.
    """
    active_agent = agent or create_search_agent(llm=llm)
    logger.info(f"Invoking Search Agent with query: '{query}'")
    
    try:
        if hasattr(active_agent, "invoke"):
            result = active_agent.invoke({"messages": [HumanMessage(content=query)]})
            return result
        else:
            return active_agent(query)
    except Exception as e:
        logger.error(f"Agent execution error: {e}")
        return {"error": str(e), "query": query}
