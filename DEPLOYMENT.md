# Deployment Guide - Finance RAG Assistant

## Quick Start (Render.com - Recommended)

### Step 1: Prepare Your Repository

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/finance-rag.git
git push -u origin main
```

2. Create `.env` file in root with:
```
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=Aniruddha Routh
```

### Step 2: Deploy to Render

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `finance-rag`
   - **Runtime**: `Docker`
   - **Build Command**: (leave empty - uses Dockerfile)
   - **Start Command**: (leave empty - uses Dockerfile)
5. Add Environment Variables:
   - `GROQ_API_KEY` = your API key from https://console.groq.com
   - `SECRET_KEY` = your password (default: "Aniruddha Routh")
6. Click "Deploy"

Your app will be live at: `https://finance-rag-xxxx.onrender.com`

---

## Docker Deployment (Local/VPS)

### Build and Run Locally

```bash
# Build the image
docker build -t finance-rag .

# Run the container
docker run -p 8000:8000 \
  -e GROQ_API_KEY=your_key \
  -e SECRET_KEY="Aniruddha Routh" \
  -v $(pwd)/chroma_db:/app/chroma_db \
  finance-rag
```

### Docker Compose (Easier)

```bash
# Start the services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Deployment on Other Platforms

### AWS EC2
1. Launch EC2 instance (Ubuntu 22.04)
2. Install Docker:
```bash
sudo apt update
sudo apt install docker.io docker-compose
```
3. Clone repo and run: `docker-compose up -d`
4. Get static IP and point domain
5. Use reverse proxy (Nginx) for HTTPS

### DigitalOcean App Platform
1. Create new app
2. Connect GitHub repo
3. Select Dockerfile
4. Add environment variables
5. Deploy

### Heroku
⚠️ Heroku free tier ended, but can use Dokku on VPS

---

## Security Best Practices

### 1. Environment Variables
✅ Never commit `.env` to git
✅ Use `.env.example` to show template
✅ Set `SECRET_KEY` to strong password in production

```bash
# Generate strong secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. HTTPS/SSL
- Use Let's Encrypt (free)
- Render provides HTTPS automatically
- For VPS: Use Nginx + Certbot

### 3. Rate Limiting (Optional)
Add to `app/main.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/ask")
@limiter.limit("10/minute")
async def ask_question(...):
    ...
```

Then add to requirements.txt: `slowapi`

### 4. Authentication Hardening
- Current: HMAC-SHA256 with Bearer token
- Consider: JWT tokens with expiration
- Consider: Rate limiting per user
- Consider: API key rotation

### 5. Data Protection
- Store uploaded PDFs securely (currently deleted after processing)
- Encrypt ChromaDB data at rest
- Regular backups of `chroma_db/`

### 6. Logging & Monitoring
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/ask")
async def ask_question(...):
    logger.info(f"Question asked: {body.question[:50]}...")
```

---

## Production Checklist

- [ ] `.env` file created with real GROQ_API_KEY
- [ ] SECRET_KEY changed to strong password
- [ ] Code pushed to private GitHub repo
- [ ] Docker image builds successfully
- [ ] CORS configured for your domain
- [ ] HTTPS enabled
- [ ] Rate limiting configured
- [ ] Monitoring/alerts set up
- [ ] Backup strategy for chroma_db/
- [ ] Domain pointing to app
- [ ] Password shared securely with users

---

## Environment Variables Reference

| Variable | Default | Purpose |
|----------|---------|---------|
| `GROQ_API_KEY` | None (Required) | Groq API authentication |
| `SECRET_KEY` | `Aniruddha Routh` | Password for login |

---

## Troubleshooting

### "Address already in use"
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### "ModuleNotFoundError"
```bash
# Rebuild Docker image
docker build --no-cache -t finance-rag .
```

### "GROQ_API_KEY not found"
```bash
# Make sure .env exists and docker-compose passes it
docker-compose config | grep GROQ_API_KEY
```

---

## Cost Estimates (2024)

| Platform | Cost | Notes |
|----------|------|-------|
| **Render** | $0-7/month | Free tier + paid when needed |
| **DigitalOcean** | $4-6/month | Small droplet |
| **AWS** | ~$10-20/month | t3.micro eligible for free tier |
| **Groq API** | Free-$1 | Free tier generous, ~5k req/month |

**Total: $0-30/month** for production deployment