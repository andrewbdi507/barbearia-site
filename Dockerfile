# ============================================================
# AGENDA OS — Render.com Dockerfile (Production)
# ============================================================
# Simplified single-stage build optimized for Render.com.
# Render auto-detects Dockerfile in root directory.
#
# Health check: GET /health
# Port: 8000 (Render injects PORT env var automatically)
# ============================================================

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---- Copy only backend ----
COPY backend/pyproject.toml backend/README.md ./

# Install Python deps via pip (Render-friendly, no uv)
RUN pip install --no-cache-dir \
    fastapi[standard] \
    uvicorn[standard] \
    sqlalchemy[asyncio] \
    asyncpg \
    psycopg2-binary \
    alembic \
    pydantic \
    pydantic-settings \
    redis \
    "python-jose[cryptography]" \
    "passlib[bcrypt]" \
    argon2-cffi \
    python-multipart \
    httpx \
    structlog \
    orjson \
    uuid7

# ---- Cache-bust: forces fresh COPY on every deploy ----
ARG CACHEBUST=1
RUN echo "Cache bust: ${CACHEBUST}"

# Copy backend source
COPY backend/ .

# Copy agents integration modules
COPY repos/ repos/

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=15s \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Copy and run startup script (parses DATABASE_URL, runs migrations, starts server)
COPY backend/start.sh /app/start.sh
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]
