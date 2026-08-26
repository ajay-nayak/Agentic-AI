"""Showcase Web Application Launcher."""

import sys
import webbrowser
import threading
import time
from pathlib import Path

# Add repo root and shared path
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import uvicorn


def open_browser():
    """Opens browser automatically after short startup delay."""
    time.sleep(1.2)
    try:
        webbrowser.open("http://127.0.0.1:8000")
    except Exception:
        pass


def main():
    print("\n========================================================")
    print("  🚀 Launching Agentic AI Showcase Web Application")
    print("========================================================")
    print("  Local URL: http://127.0.0.1:8000")
    print("  API Docs:  http://127.0.0.1:8000/docs")
    print("========================================================\n")
    
    # Launch browser on separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    uvicorn.run(
        "web.backend.app:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
