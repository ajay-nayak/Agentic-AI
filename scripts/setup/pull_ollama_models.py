"""Script to download required local Ollama models."""

import shutil
import subprocess
import sys

RECOMMENDED_MODELS = [
    "gemma4:e2b",
    "gemma3:1b",
    "gemma3:270m",
    "llama3.2:3b",
]


def main():
    print("========================================================")
    print("  Ollama Model Pulling Utility for Agentic AI")
    print("========================================================\n")
    
    ollama_path = shutil.which("ollama")
    if not ollama_path:
        print("❌ Error: Ollama CLI not found. Please install Ollama from https://ollama.com/")
        sys.exit(1)
        
    print("Recommended models for this repository:")
    for i, model in enumerate(RECOMMENDED_MODELS, 1):
        print(f"  {i}. {model}")
        
    print("\nStarting downloads (press Ctrl+C to cancel)...\n")
    for model in RECOMMENDED_MODELS:
        print(f"--> Pulling model: {model}")
        try:
            subprocess.run(["ollama", "pull", model], check=True)
            print(f"✅ Successfully pulled {model}\n")
        except Exception as e:
            print(f"⚠️  Could not pull {model}: {e}\n")


if __name__ == "__main__":
    main()
