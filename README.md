# Finance RAG Assistant 💰

A secure, AI-powered Retrieval-Augmented Generation (RAG) application that answers questions about your bank statements using advanced LLMs.

## Features

✅ **Secure Authentication** - HMAC-SHA256 password hashing  
✅ **PDF Processing** - Extract and analyze bank statements  
✅ **AI-Powered Q&A** - Groq LLM with local embeddings  
✅ **Vector Search** - ChromaDB for semantic similarity  
✅ **Beautiful UI** - Modern, responsive frontend  
✅ **Docker Ready** - Easy containerized deployment  
✅ **100% Free** - Groq + Render free tiers  

## Quick Start

### Prerequisites
- Python 3.13+
- Groq API key (free at https://console.groq.com)

### Local Development

```bash
# Clone & setup
git clone <repo>
cd finance-rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirement.txt

# Create .env file
cp .env.example .env
# Edit .env with your GROQ_API_KEY

# Run locally
uvicorn app.main:app --reload
```

Visit **http://localhost:8000** and log in with passkey (contact the author)

### Docker Deployment

```bash
# Build image
docker build -t finance-rag .

# Run container
docker run -p 8000:8000 \
  -e GROQ_API_KEY=your_key \
  -e SECRET_KEY="--" \
  -v $(pwd)/chroma_db:/app/chroma_db \
  finance-rag
```

Or with Docker Compose:
```bash
docker-compose up -d
```

## Deployment

🚀 **Recommended: Render.com (Free)**

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Step-by-step Render deployment
- AWS, DigitalOcean, Heroku options
- Security best practices
- Production checklist

## Architecture

```
┌─────────────┐
│   Browser   │ ← Modern React-like UI
└──────┬──────┘
       │ HTTPS
       ↓
┌─────────────────────┐
│   FastAPI Server    │
├─────────────────────┤
│  /upload  - Protected
│  /ask     - Protected
│  /        - Public
└──────┬──────────────┘
       │
       ├→ PDF Processing (PyPDF)
       ├→ Text Chunking (LangChain)
       ├→ Embeddings (HuggingFace Local)
       ├→ Vector DB (ChromaDB)
       └→ LLM (Groq API)
```

## API

### Authenticate
All protected endpoints require `Authorization: Bearer <password>` header

### POST `/upload`
Upload and process a PDF file
```bash
curl -X POST http://localhost:8000/upload \
  -H "Authorization: Bearer password" \
  -F "file=@statement.pdf"
```

Response:
```json
{
  "message": "Ingested 'statement.pdf' successfully."
}
```

### POST `/ask`
Ask a question about uploaded documents
```bash
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer aa aa" \
  -H "Content-Type: application/json" \
  -d '{"question": "What was my closing balance?"}'
```

Response:
```json
{
  "answer": "$10,556.65",
  "sources": [
    "SAMPLE BANK STATEMENT\nAccount Holder: John Smith\n..."
  ]
}
```

## Security

- **Passwords**: Hashed with HMAC-SHA256 (one-way encryption)
- **Authentication**: Bearer tokens in Authorization header
- **Data**: PDFs processed in-memory, only embeddings stored
- **Non-root**: Docker runs as unprivileged user
- **HTTPS**: Recommended for production (Render provides auto)

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `GROQ_API_KEY` | Required | Groq API authentication |
| `SECRET_KEY` | `aa aa` | Login password |

## Project Structure

```
finance-rag/
├── app/
│   ├── main.py          # FastAPI routes & auth
│   ├── rag.py           # RAG pipeline & LLM
│   └── ingest.py        # PDF processing
├── index.html           # Frontend UI
├── chroma_db/           # Vector database
├── data/                # Sample PDFs
├── Dockerfile           # Container image
├── docker-compose.yml   # Multi-container setup
├── requirement.txt      # Python dependencies
└── DEPLOYMENT.md        # Deployment guide
```

## Technologies

- **Backend**: FastAPI, Uvicorn
- **LLM**: Groq (Llama 3.1)
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB
- **Document Processing**: LangChain, PyPDF
- **Frontend**: HTML/CSS/JavaScript
- **Container**: Docker

## Performance

- **Latency**: 2-3s per question (Groq API)
- **Throughput**: ~30-50 requests/minute (free tier)
- **Model Size**: ~100MB (embeddings downloaded on first use)
- **Database**: ~1MB per 50 PDF pages

## Limitations

- **File Size**: Tested up to 50MB PDFs
- **Rate Limit**: Groq free tier ~5k requests/month
- **Storage**: Render free tier: 0.5GB ephemeral
- **Timeout**: 30s API response timeout

## Development

```bash
# Run tests
pytest

# Format code
black app/

# Type check
mypy app/

# Lint
flake8 app/
```

## Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create feature branch: `git checkout -b feature/xyz`
3. Commit changes: `git commit -am 'Add feature'`
4. Push: `git push origin feature/xyz`
5. Create Pull Request

## License

MIT License - See LICENSE file

## Support

- **Issues**: GitHub Issues
- **Docs**: DEPLOYMENT.md for setup help
- **API Key**: https://console.groq.com

---

**Made with ❤️ for secure document analysis**
