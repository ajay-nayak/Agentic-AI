"""Environment variable loader helper with hierarchy support."""

import os
from pathlib import Path
from dotenv import load_dotenv


def load_project_env(project_root: str | Path | None = None) -> bool:
    """
    Loads environment variables with fallback from project directory to repo root.
    
    Args:
        project_root: Optional path to project root. Defaults to current working directory.
        
    Returns:
        bool: True if at least one .env file was successfully found and loaded.
    """
    loaded = False
    
    # 1. Try project-specific .env if project_root provided
    if project_root:
        proj_env = Path(project_root) / ".env"
        if proj_env.exists():
            load_dotenv(dotenv_path=proj_env, override=False)
            loaded = True
            
    # 2. Try current working directory
    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        load_dotenv(dotenv_path=cwd_env, override=False)
        loaded = True
        
    # 3. Try repo root (traverse upwards until .git or pyproject.toml is found)
    current = Path(__file__).resolve().parent
    while current.parent != current:
        root_env = current / ".env"
        if root_env.exists() and root_env != cwd_env:
            load_dotenv(dotenv_path=root_env, override=False)
            loaded = True
            break
        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            break
        current = current.parent
        
    return loaded
