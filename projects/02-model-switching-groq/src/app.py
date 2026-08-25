"""CLI Runner and Interactive Exercise for Project 02: Model Switching (Groq)."""

import argparse
from shared.python.utils.logger import get_logger
from shared.python.utils.env_loader import load_project_env
try:
    from .model_switcher import GroqModelSwitcher, compare_models, VALID_GROQ_MODELS
except (ImportError, ValueError):
    from model_switcher import GroqModelSwitcher, compare_models, VALID_GROQ_MODELS

load_project_env()
logger = get_logger("02-model-switching-groq")


def main():
    parser = argparse.ArgumentParser(description="Groq Model Switching and Comparison Runner")
    parser.add_argument("--prompt", default="Explain the concept of machine learning in one clear sentence.", help="Prompt to test")
    parser.add_argument("--mock", action="store_true", help="Force mock mode without calling live Groq APIs")
    args = parser.parse_args()

    print("\n========================================================")
    print("  02 - Groq Model Switching & Multi-Model Comparison")
    print("========================================================\n")
    
    print(f"Supported Models: {', '.join(VALID_GROQ_MODELS)}\n")
    print(f"Testing Prompt: \"{args.prompt}\"\n")

    print("[1] Querying Models & Benchmarking Output:")
    print("--------------------------------------------------------")
    results = compare_models(args.prompt, use_mock=args.mock)
    
    for model_name, output in results.items():
        print(f"\nModel: [{model_name}]")
        print(f"Response: {output}")

    print("\n========================================================")
    print("Execution complete.")


if __name__ == "__main__":
    main()
