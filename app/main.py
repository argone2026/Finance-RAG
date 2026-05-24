"""
main.py — FastAPI server
  GET  /      — serve frontend
  POST /upload  — ingest a PDF into ChromaDB
  POST /ask     — ask a question about the uploaded statement
"""
import os
import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.ingest import ingest
from app.rag import ask

app = FastAPI(title="Finance RAG Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a bank statement PDF and ingest it into the vector store."""
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        ingest(tmp_path)
        Path(tmp_path).unlink()
        return {"message": f"Ingested '{file.filename}' successfully."}
    except ValueError as e:
        Path(tmp_path).unlink()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        Path(tmp_path).unlink()
        raise HTTPException(status_code=500, detail=f"Failed to ingest PDF: {str(e)}")


class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
async def ask_question(body: QuestionRequest):
    """Ask a question about your uploaded bank statement."""
    
    try:
        result = ask(body.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {str(e)}")


@app.get("/")
def root():
    """Serve the frontend UI"""
    index_path = Path(__file__).parent.parent / "index.html"
    return FileResponse(index_path)


@app.get("/favicon.ico")
def favicon():
    """Serve favicon"""
    favicon_path = Path(__file__).parent.parent / "favicon.ico"
    if favicon_path.exists():
        return FileResponse(favicon_path, media_type="image/x-icon")
    return {"status": "not found"}
