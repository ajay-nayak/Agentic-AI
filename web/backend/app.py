"""FastAPI Server for Agentic AI Showcase Web Application."""

import os
import sys
import time
import io
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Ensure repo root and projects are on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SHARED_DIR = REPO_ROOT / "shared" / "python"
PROJECT_01_SRC = REPO_ROOT / "projects" / "01-llm-chains-and-prompts" / "src"
PROJECT_03_SRC = REPO_ROOT / "projects" / "03-ai-search-agent" / "src"
PROJECT_04_SRC = REPO_ROOT / "projects" / "04-langgraph-state-workflows" / "src"

for p in [REPO_ROOT, SHARED_DIR, PROJECT_01_SRC, PROJECT_03_SRC, PROJECT_04_SRC]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from shared.python.utils.env_loader import load_project_env
from shared.python.utils.logger import get_logger
from shared.python.utils.model_factory import get_chat_model

# Project 01
from summarizer import summarize_text, extract_facts

# Project 03
from agent import create_search_agent, run_search_agent

load_project_env()
logger = get_logger("web-showcase")

app = FastAPI(
    title="Agentic AI Showcase API",
    description="Interactive backend API for Agentic AI projects",
    version="0.1.0",
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf", ".json", ".csv", ".py", ".log", ".rst"}


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extracts raw text content from uploaded file bytes."""
    ext = Path(filename).suffix.lower()
    
    if ext == ".pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text_pages = [page.extract_text() or "" for page in reader.pages]
            full_text = "\n\n".join(text_pages).strip()
            if not full_text:
                raise ValueError("PDF file contains no extractable text.")
            return full_text
        except ImportError:
            raise HTTPException(status_code=500, detail="pypdf package is not installed.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {str(e)}")
            
    # For text-based formats
    for encoding in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
        try:
            return file_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue
            
    raise HTTPException(status_code=400, detail="Unable to decode text file. Please upload a UTF-8 compatible file.")


class SearchRequest(BaseModel):
    query: str
    provider: str = "ollama"
    model: Optional[str] = None


@app.get("/api/v1/health")
async def health_check():
    """Returns server and LLM configuration status."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "providers": ["ollama", "openai", "groq"],
        "max_file_size_mb": 5,
        "allowed_extensions": sorted(list(ALLOWED_EXTENSIONS)),
    }


@app.post("/api/v1/process-text")
async def process_text(
    action: str = Form("summary"),
    provider: str = Form("ollama"),
    model: Optional[str] = Form(None),
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    """
    Processes document text for Summarization, Facts Extraction, or Full Analysis.
    Supports direct text paste or file uploads up to 5MB.
    """
    input_text = ""
    source_info = "direct_input"
    
    # 1. Process uploaded file if present
    if file and file.filename:
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
            )
            
        file_bytes = await file.read()
        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size ({len(file_bytes) / (1024*1024):.2f} MB) exceeds maximum allowed limit of 5 MB.",
            )
            
        input_text = extract_text_from_file(file_bytes, file.filename)
        source_info = f"file:{file.filename}"
    elif text and text.strip():
        input_text = text.strip()
    else:
        raise HTTPException(
            status_code=400,
            detail="Please provide text in the text box or upload a document file.",
        )

    if len(input_text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Input text is too short to analyze (minimum 10 characters).")

    # 2. Invoke appropriate LCEL chain
    start_time = time.time()
    try:
        chat_model = get_chat_model(provider=provider, model_name=model)
        
        if action == "facts":
            result = extract_facts(input_text, llm=chat_model)
        elif action == "summary":
            result = summarize_text(input_text, llm=chat_model, mode="summary")
        else:
            result = summarize_text(input_text, llm=chat_model, mode="full")
            
        duration_ms = int((time.time() - start_time) * 1000)
        
        return {
            "status": "success",
            "action": action,
            "source": source_info,
            "output": result,
            "duration_ms": duration_ms,
            "word_count": len(input_text.split()),
            "char_count": len(input_text),
            "provider": provider,
            "model": model or "default",
        }
    except Exception as e:
        logger.error(f"Text processing error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"LLM processing error with provider '{provider}': {str(e)}",
        )


@app.post("/api/v1/search")
async def search_agent(req: SearchRequest):
    """Executes the Autonomous ReAct AI Search Agent."""
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
        
    start_time = time.time()
    try:
        chat_model = get_chat_model(provider=req.provider, model_name=req.model, temperature=0.1)
        agent = create_search_agent(llm=chat_model)
        raw_response = run_search_agent(req.query.strip(), agent=agent)
        
        # Format response
        if isinstance(raw_response, dict):
            if "messages" in raw_response:
                messages = raw_response["messages"]
                output_text = messages[-1].content if messages else str(raw_response)
            elif "output" in raw_response:
                output_text = raw_response["output"]
            else:
                output_text = str(raw_response)
        else:
            output_text = str(raw_response)
            
        duration_ms = int((time.time() - start_time) * 1000)
        
        return {
            "status": "success",
            "query": req.query,
            "output": output_text,
            "duration_ms": duration_ms,
            "provider": req.provider,
            "model": req.model or "default",
        }
    except Exception as e:
        logger.error(f"Search agent execution error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Search agent execution failed with provider '{req.provider}': {str(e)}",
        )


# Static files mount & Web Root
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    """Serves the showcase frontend."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return JSONResponse({"message": "Agentic AI Showcase API running. index.html not found."})
