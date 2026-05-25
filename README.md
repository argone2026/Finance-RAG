# Finance RAG Assistant 💰

An AI-powered Retrieval-Augmented Generation (RAG) application that answers questions about your bank statements using advanced LLMs.

## Quick Start (Local Setup)

### Prerequisites
- Python 3.13+
- Groq API key (free at https://console.groq.com)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/argone2026/Finance-RAG.git
cd Finance-RAG

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirement.txt

# 4. Create .env file and add your API key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# 5. Run the app
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access the App
Open your browser: **http://localhost:8000**

## How It Works

1. **Upload PDF** - Add your bank statement
2. **Ask Questions** - Ask anything about your statement
3. **Get Answers** - AI analyzes the document and responds

### Example Questions
- "What was my closing balance?"
- "How many transactions did I make?"
- "What was the largest deposit?"


---

## Demo Video

📹 **[Watch how it works locally](INSERT_VIDEO_LINK_HERE)**

*(Add your video link here to show the app in action)*

---

## Features

✅ PDF document upload and processing  
✅ AI-powered Q&A with Groq LLM  
✅ Semantic search with local embeddings  
✅ Vector database (ChromaDB)  
✅ Clean, minimal UI  
✅ Works entirely locally

## Architecture

```
Browser (UI)
    ↓
FastAPI Server (Port 8000)
    ↓
┌─────────────────────┐
│  PDF Processing     │ → PyPDF, LangChain
│  Embeddings         │ → HuggingFace (local)
│  Vector Database    │ → ChromaDB
│  LLM Generation     │ → Groq API
└─────────────────────┘
```

## API Endpoints

### POST `/upload`
Upload a PDF file for analysis

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@statement.pdf"
```

### POST `/ask`
Ask a question about uploaded documents

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What was my closing balance?"}'
```

Response:
```json
{
  "answer": "$10,556.65",
  "sources": ["...document excerpt..."]
}
```

---

## Project Structure

```
finance-rag/
├── app/
│   ├── main.py          # FastAPI server
│   ├── ingest.py        # PDF processing
│   └── rag.py           # Q&A pipeline
├── index.html           # Web UI
├── chroma_db/           # Vector database
├── data/                # Sample PDFs
├── requirement.txt      # Dependencies
└── README.md            # This file
```

---

## Technologies Used

- **Backend**: FastAPI, Uvicorn
- **LLM**: Groq (Llama 3.1 70B)
- **Embeddings**: HuggingFace Sentence Transformers
- **Vector DB**: ChromaDB
- **Document Processing**: LangChain, PyPDF
- **Frontend**: HTML/CSS/JavaScript

---

## Troubleshooting

**Port 8000 already in use?**
```bash
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

**Model download fails?**
The embedding model (87MB) downloads on first use. Ensure stable internet connection.

**GROQ_API_KEY error?**
Make sure `.env` file exists and contains a valid Groq API key.

---

## Local Testing

### Test with sample PDF
```bash
python create_minimal_pdf.py
curl -X POST http://localhost:8000/upload -F "file=@data/minimal_test.pdf"
```

### Test Q&A
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What was the closing balance?"}'
```

---

## Performance

- Response time: 2-3 seconds per question
- Model size: ~100MB (downloaded once)
- Storage: ~1MB per 50 pages of PDF

---

## Notes

- This app is designed for **local use**
- All processing happens on your machine
- No data is stored on external servers (except Groq API calls)
- PDFs are processed in-memory for security

---

## License

MIT
