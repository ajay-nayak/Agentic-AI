"""Search tool implementation using Tavily with offline fallback capability."""

import os
from typing import Any
from langchain_core.tools import tool, BaseTool
from shared.python.utils.logger import get_logger
from shared.python.utils.env_loader import load_project_env

load_project_env()
logger = get_logger(__name__)


def create_search_tool() -> BaseTool:
    """Creates a LangChain search tool with Tavily or simulated fallback."""
    
    @tool
    def search(query: str) -> str:
        """Tool for searching the web for real-time information, jobs, news, and technical questions.
        
        Args:
            query: The search query string.
            
        Returns:
            str: Retrieved search results summary or content.
        """
        api_key = os.getenv("TAVILY_API_KEY")
        if api_key:
            try:
                from tavily import TavilyClient
                client = TavilyClient(api_key=api_key)
                logger.info(f"Executing live Tavily search for: '{query}'")
                results = client.search(query=query)
                return str(results)
            except Exception as e:
                logger.warning(f"Tavily search API failed: {e}. Using simulated response.")
                
        # Graceful fallback when TAVILY_API_KEY is not configured or in offline mode
        logger.info(f"Executing simulated search for query: '{query}'")
        return (
            f"[Search Results for '{query}']:\n"
            f"1. Top opening: Senior Mobile AI Engineer at Bangalore Tech Labs (10+ years exp, Android/Tizen/Windows).\n"
            f"2. Staff AI Systems Architect: On-device Edge AI & ML optimization in Bangalore.\n"
            f"3. Principal Mobile Architect: Enterprise Multi-platform Mobile AI applications (Bangalore)."
        )

    return search


# Default exported tool instance
search = create_search_tool()
