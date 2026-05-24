"""
main.py — FastAPI server
  GET  /      — serve frontend
  POST /upload  — ingest a PDF into ChromaDB
  POST /ask     — ask a question about the uploaded statement
"""
import os
import shutil
import tempfile
import hashlib
import hmac
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Header
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

# Password hashing setup using HMAC-SHA256
PLAINTEXT_PASSWORD = os.getenv("SECRET_KEY", "Aniruddha Routh")
HASH_SALT = "finance-rag-salt-2026"
PASSWORD_HASH = hashlib.sha256((HASH_SALT + PLAINTEXT_PASSWORD).encode()).hexdigest()


def verify_auth(authorization: str = Header(None)):
    """Verify authentication token using HMAC-SHA256 comparison"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Unauthorized")
    except ValueError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Hash the provided password and compare with stored hash
    token_hash = hashlib.sha256((HASH_SALT + token).encode()).hexdigest()
    
    # Use constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(token_hash, PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return True


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), authorization: str = Header(None)):
    """Upload a bank statement PDF and ingest it into the vector store."""
    verify_auth(authorization)
    
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
async def ask_question(body: QuestionRequest, authorization: str = Header(None)):
    """Ask a question about your uploaded bank statement."""
    verify_auth(authorization)
    
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
