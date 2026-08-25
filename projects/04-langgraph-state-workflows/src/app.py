"""CLI Runner for Project 04: LangGraph State Workflows."""

import argparse
from shared.python.utils.logger import get_logger
try:
    from .workflow import run_research_workflow
except (ImportError, ValueError):
    from workflow import run_research_workflow

logger = get_logger("04-langgraph-state-workflows")


def main():
    parser = argparse.ArgumentParser(description="LangGraph State Workflows Runner")
    parser.add_argument(
        "--query",
        default="Compare and analyze LangChain LCEL vs LangGraph cyclic state machines.",
        help="Input query to process through the state graph"
    )
    args = parser.parse_args()

    print("\n========================================================")
    print("  04 - LangGraph State Workflows & Conditional Routing")
    print("========================================================\n")
    print(f"User Query: \"{args.query}\"\n")

    print("[1] Executing StateGraph...")
    print("--------------------------------------------------------")
    final_state = run_research_workflow(args.query)

    print(f"\nFinal Classification: is_complex = {final_state.get('is_complex')}")
    print(f"Total Graph Iterations: {final_state.get('iteration_count')}")
    print(f"\nResearch Notes Accumulated ({len(final_state.get('research_notes', []))}):")
    for note in final_state.get("research_notes", []):
        print(f"  • {note}")

    print(f"\nFinal Answer:\n{final_state.get('final_answer')}")
    print("\n========================================================")


if __name__ == "__main__":
    main()
