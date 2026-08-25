"""CLI Runner for Project 03: AI Search Agent."""

import argparse
from shared.python.utils.logger import get_logger
from shared.python.utils.env_loader import load_project_env
from shared.python.utils.model_factory import get_chat_model
try:
    from .agent import create_search_agent, run_search_agent
except (ImportError, ValueError):
    from agent import create_search_agent, run_search_agent

load_project_env()
logger = get_logger("03-ai-search-agent")


def main():
    parser = argparse.ArgumentParser(description="Autonomous ReAct Search Agent Runner")
    parser.add_argument(
        "--query",
        default="Look for 3 job openings for senior mobile developer with AI & ML exposure in Bangalore with 10+ years experience.",
        help="Query for the search agent"
    )
    parser.add_argument("--provider", default="ollama", choices=["ollama", "openai", "groq"], help="LLM Provider")
    parser.add_argument("--model", default=None, help="Specific model name")
    args = parser.parse_args()

    print("\n========================================================")
    print("  03 - Autonomous AI Search Agent (ReAct + Tool Calling)")
    print("========================================================\n")
    print(f"Target Query: \"{args.query}\"\n")
    print(f"Provider: {args.provider} (Model: {args.model or 'default'})\n")

    try:
        model = get_chat_model(provider=args.provider, model_name=args.model, temperature=0.1)
        agent = create_search_agent(llm=model)
        
        print("Invoking Agent Loop...")
        print("--------------------------------------------------------")
        response = run_search_agent(args.query, agent=agent)
        print("\nAgent Execution Output:")
        print(response)
        
    except Exception as e:
        logger.error(f"Failed to execute Search Agent: {e}")
        print(f"\nNotice: LLM service connection error. Check if '{args.provider}' is accessible.")


if __name__ == "__main__":
    main()
