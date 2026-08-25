"""Repository Structure & Integrity Validator."""

import sys
import py_compile
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

REQUIRED_ROOT_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    ".gitignore",
    ".env.example",
    "pyproject.toml",
]

REQUIRED_DOCS = [
    "docs/architecture/agentic-ai-patterns.md",
    "docs/architecture/frontend-integration.md",
    "docs/concepts/langchain-fundamentals.md",
    "docs/concepts/langgraph-state-workflows.md",
    "docs/guides/environment-setup.md",
    "docs/guides/ollama-local-llms.md",
    "docs/guides/langsmith-tracing.md",
    "docs/repository-reorganization-report.md",
]

REQUIRED_PROJECTS = [
    "projects/01-llm-chains-and-prompts",
    "projects/02-model-switching-groq",
    "projects/03-ai-search-agent",
    "projects/04-langgraph-state-workflows",
]


def check_files():
    print("[1] Checking Required Root Files...")
    missing = []
    for f in REQUIRED_ROOT_FILES:
        path = REPO_ROOT / f
        if not path.exists():
            print(f"  ❌ Missing: {f}")
            missing.append(f)
        else:
            print(f"  ✅ Found: {f}")

    print("\n[2] Checking Required Documentation...")
    for d in REQUIRED_DOCS:
        path = REPO_ROOT / d
        if not path.exists():
            print(f"  ❌ Missing: {d}")
            missing.append(d)
        else:
            print(f"  ✅ Found: {d}")

    print("\n[3] Checking Projects Structure...")
    for p in REQUIRED_PROJECTS:
        proj_dir = REPO_ROOT / p
        if not proj_dir.exists():
            print(f"  ❌ Missing project directory: {p}")
            missing.append(p)
            continue
        
        # Check sub-files
        sub_items = ["README.md", "pyproject.toml", "src", "tests"]
        sub_missing = [s for s in sub_items if not (proj_dir / s).exists()]
        if sub_missing:
            print(f"  ❌ Project {p} missing: {sub_missing}")
            missing.extend([f"{p}/{s}" for s in sub_missing])
        else:
            print(f"  ✅ Valid Project: {p}")

    print("\n[4] Compiling Python Files for Syntax Validation...")
    syntax_errors = 0
    for py_file in REPO_ROOT.rglob("*.py"):
        if ".venv" in py_file.parts or ".pytest_cache" in py_file.parts:
            continue
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            print(f"  ❌ Syntax Error in {py_file}: {e}")
            syntax_errors += 1
            
    if syntax_errors == 0:
        print("  ✅ All Python files passed syntax validation.")

    return len(missing) == 0 and syntax_errors == 0


def main():
    print("========================================================")
    print("  Agentic AI Repository Integrity Validation")
    print("========================================================\n")
    
    valid = check_files()
    
    print("\n========================================================")
    if valid:
        print("  🎉 Repository integrity check PASSED!")
    else:
        print("  ❌ Repository integrity check FAILED.")
    print("========================================================\n")
    
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
