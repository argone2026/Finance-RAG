# Production Security Configuration

## CORS Setup

For production, restrict CORS to your domain:

```python
# In app/main.py
from fastapi.middleware.cors import CORSMiddleware

# Change from "*" to specific domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## HTTPS/SSL

### Render (Automatic)
- ✅ Free HTTPS provided automatically
- ✅ Auto-renewal of certificates
- ✅ Enforced HTTPS redirects

### VPS with Nginx + Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

Nginx config:
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name yourdomain.com;
        return 301 https://$server_name$request_uri;
    }
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Rate Limiting

Add to `requirement.txt`:
```
slowapi==0.1.9
```

Update `app/main.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Max 10 requests/minute"}
    )

# Apply to endpoints
@app.post("/upload")
@limiter.limit("5/minute")
async def upload_pdf(...):
    ...

@app.post("/ask")
@limiter.limit("10/minute")
async def ask_question(...):
    ...
```

## Environment-Specific Configuration

Create separate `.env` files:

### `.env.development`
```
GROQ_API_KEY=sk_...
SECRET_KEY=dev_password_123
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1
```

### `.env.production`
```
GROQ_API_KEY=sk_prod_...
SECRET_KEY=[strong_random_key]
DEBUG=false
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Logging & Monitoring

### Structured Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# Setup logging
logger = logging.getLogger(__name__)
handler = RotatingFileHandler(
    'app.log',
    maxBytes=10485760,  # 10MB
    backupCount=10
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.post("/ask")
async def ask_question(body: QuestionRequest, authorization: str = Header(None)):
    verify_auth(authorization)
    logger.info(f"Question received: {body.question[:50]}...")
    
    try:
        result = ask(body.question)
        logger.info(f"Success: returned answer")
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise
```

## Database Backups

### Automated Backups (Cron)

```bash
# Create backup script: backup.sh
#!/bin/bash
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf $BACKUP_DIR/chroma_db_$TIMESTAMP.tar.gz chroma_db/

# Keep only last 7 backups
find $BACKUP_DIR -name "chroma_db_*.tar.gz" -mtime +7 -delete
```

Add to crontab:
```bash
crontab -e
# Daily backup at 2 AM
0 2 * * * /app/backup.sh
```

## DDoS Protection

### Render
- ✅ Built-in DDoS protection
- ✅ Automatic rate limiting
- ✅ WAF included

### VPS with Fail2Ban
```bash
# Install
sudo apt install fail2ban

# Configure
sudo nano /etc/fail2ban/jail.d/uvicorn.conf
```

Content:
```
[uvicorn-auth]
enabled = true
port = http,https
filter = uvicorn-auth
logpath = /app/app.log
maxretry = 5
findtime = 600
bantime = 3600
```

## API Key Rotation

For production multi-user setup:
```python
# Database model (example with SQLAlchemy)
class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key_hash = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

# Validate key
def verify_api_key(api_key: str):
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    db_key = db.query(APIKey).filter(
        APIKey.key_hash == key_hash,
        APIKey.is_active == True,
        APIKey.expires_at > datetime.utcnow()
    ).first()
    
    if not db_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return db_key
```

## Security Headers

Add to `app/main.py`:
```python
from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(
    middleware=[
        Middleware(
            TrustedHostMiddleware,
            allowed_hosts=["yourdomain.com", "www.yourdomain.com"]
        ),
    ]
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

## Checklist

- [ ] CORS restricted to your domain
- [ ] HTTPS enabled with valid certificate
- [ ] Rate limiting configured
- [ ] Logging and monitoring active
- [ ] Automated backups set up
- [ ] DDoS protection enabled
- [ ] API key rotation implemented
- [ ] Security headers added
- [ ] Environment variables secured
- [ ] Database encrypted at rest (if applicable)
- [ ] Regular dependency updates scheduled
- [ ] Incident response plan documented