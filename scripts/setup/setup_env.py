"""Automated Environment Setup and Verification Script for Agentic AI Repository."""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def check_python_version():
    print(f"[1] Python Version: {sys.version.split()[0]}")
    if sys.version_info < (3, 11):
        print("  ❌ Warning: Python 3.11+ is recommended.")
        return False
    print("  ✅ Python version is compatible.")
    return True


def check_env_file():
    print("\n[2] Checking Environment Configuration (.env)...")
    env_file = REPO_ROOT / ".env"
    env_example = REPO_ROOT / ".env.example"
    
    if env_file.exists():
        print("  ✅ '.env' file exists.")
    else:
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print("  ⚠️  Created '.env' from '.env.example'. Please fill in your API keys if needed.")
        else:
            print("  ❌ Neither '.env' nor '.env.example' found.")
            return False
    return True


def check_ollama():
    print("\n[3] Checking Ollama Service...")
    ollama_path = shutil.which("ollama")
    if ollama_path:
        print(f"  ✅ Ollama CLI found at: {ollama_path}")
    else:
        print("  ℹ️  Ollama CLI not found in PATH. You can install it from https://ollama.com/")


def main():
    print("========================================================")
    print("  Agentic AI Repository - Environment Setup & Check")
    print("========================================================\n")
    
    check_python_version()
    check_env_file()
    check_ollama()
    
    print("\n========================================================")
    print("  Setup check completed!")
    print("========================================================\n")


if __name__ == "__main__":
    main()
