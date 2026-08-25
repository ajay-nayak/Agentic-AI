"""CLI Runner for Project 01: LLM Chains and Prompts."""

import argparse
from shared.python.utils.logger import get_logger
from shared.python.utils.env_loader import load_project_env
from shared.python.utils.model_factory import get_chat_model

from .summarizer import summarize_text
from .password_generator import generate_password

logger = get_logger("01-llm-chains-and-prompts")


SAMPLE_ARTICLE = """Building LangChain for Mobile: How We Designed an On-Device AI Framework for iOS and Android

On-device AI is one of the most exciting shifts in mobile development. Apple Intelligence brings Foundation Models to iOS 18+. Google ships Gemini Nano via ML Kit on Android 14+. For the first time, powerful language models run natively on phones - no cloud, no latency, no privacy trade-offs.

But there's a problem: these APIs are completely different.

On iOS, you write Swift with SystemLanguageModel and @Generable. On Android, you write Kotlin with GenerativeModel from ML Kit. If you want composable chains, memory management, or a pipeline DSL - the things that made LangChain transformative for cloud LLMs - you're on your own.
"""


def main():
    load_project_env()
    
    parser = argparse.ArgumentParser(description="LangChain LCEL Chains & Prompts Demo")
    parser.add_argument("--provider", default="ollama", choices=["ollama", "openai", "groq"], help="LLM Provider")
    parser.add_argument("--model", default=None, help="Specific model name (e.g. gemma4:e2b, gpt-4o-mini)")
    parser.add_argument("--task", default="all", choices=["summarize", "password", "all"], help="Task to run")
    args = parser.parse_args()

    print("\n========================================================")
    print("  01 - LangChain LCEL Chains & Prompt Engineering Demo")
    print("========================================================\n")
    
    try:
        model = get_chat_model(provider=args.provider, model_name=args.model)
        
        if args.task in ["summarize", "all"]:
            print("\n[1] Running Summarization Chain...")
            print("--------------------------------------------------------")
            summary = summarize_text(SAMPLE_ARTICLE, llm=model)
            print(f"Summary Output:\n{summary}\n")
            
        if args.task in ["password", "all"]:
            seed = "Ajay"
            print(f"\n[2] Running Few-Shot Password Generator for seed: '{seed}'...")
            print("--------------------------------------------------------")
            passwords = generate_password(seed, llm=model)
            print(f"Generated Passwords:\n{passwords}\n")
            
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        print(f"\nNotice: Could not connect to {args.provider} LLM service. Ensure service is active or valid API keys are set.")


if __name__ == "__main__":
    main()
