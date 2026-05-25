#!/bin/sh
# Startup script for Railway/Docker - handles environment variables properly

PORT=${PORT:-8000}
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
