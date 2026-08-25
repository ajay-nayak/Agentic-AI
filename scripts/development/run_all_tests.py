"""Unified test runner across all projects and shared packages."""

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


def run_tests():
    print("========================================================")
    print("  Running Test Suites Across All Agentic AI Projects")
    print("========================================================\n")

    projects_dir = REPO_ROOT / "projects"
    project_folders = [p for p in projects_dir.iterdir() if p.is_dir() and (p / "tests").exists()]
    
    total_passed = 0
    total_failed = 0
    
    # Also test template
    template_dir = REPO_ROOT / "config" / "templates" / "project-template"
    if template_dir.exists() and (template_dir / "tests").exists():
        project_folders.append(template_dir)

    has_uv = shutil.which("uv") is not None

    for project in sorted(project_folders):
        print(f"--> Testing [{project.name}] ({project.relative_to(REPO_ROOT)})...")
        env = os.environ.copy()
        pythonpath = [
            str(REPO_ROOT),
            str(REPO_ROOT / "shared" / "python"),
            str(project),
            str(project / "src"),
        ]
        if "PYTHONPATH" in env:
            pythonpath.append(env["PYTHONPATH"])
        env["PYTHONPATH"] = os.pathsep.join(pythonpath)

        if has_uv:
            cmd = ["uv", "run", "--with", "pytest", "pytest", str(project / "tests"), "-v"]
        else:
            cmd = [sys.executable, "-m", "pytest", str(project / "tests"), "-v"]

        res = subprocess.run(cmd, cwd=str(project), env=env)
        
        if res.returncode == 0:
            print(f"  [OK] [{project.name}] PASSED\n")
            total_passed += 1
        else:
            print(f"  [FAILED] [{project.name}] FAILED\n")
            total_failed += 1

    print("========================================================")
    print(f"  Summary: {total_passed} Passed, {total_failed} Failed")
    print("========================================================")
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
