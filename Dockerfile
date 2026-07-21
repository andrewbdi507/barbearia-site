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

# Copy backend source
COPY backend/ .

# Copy agents integration modules
COPY repos/ repos/

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=15s \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Startup: parse DATABASE_URL (Render format) → DB_* vars, run migrations, start server
CMD ["sh", "-c", "\
  if [ -n \"$DATABASE_URL\" ]; then \
    echo \"Parsing DATABASE_URL...\"; \
    DB_USER=$(echo $DATABASE_URL | sed -n 's|.*://\\([^:]*\\):.*|\\1|p'); \
    DB_PASSWORD=$(echo $DATABASE_URL | sed -n 's|.*://[^:]*:\\([^@]*\\)@.*|\\1|p'); \
    DB_HOST=$(echo $DATABASE_URL | sed -n 's|.*@\\([^:/]*\\).*|\\1|p'); \
    DB_PORT=$(echo $DATABASE_URL | sed -n 's|.*:\\([0-9]*\\)/.*|\\1|p'); \
    DB_NAME=$(echo $DATABASE_URL | sed -n 's|.*/\\([^?]*\\).*|\\1|p'); \
    export DB_USER DB_PASSWORD DB_HOST DB_PORT DB_NAME; \
    echo \"DB_HOST=$DB_HOST DB_NAME=$DB_NAME\"; \
  fi; \
  echo 'Running database migrations...'; \
  PYTHONPATH=/app alembic -c /app/alembic/alembic.ini upgrade head; \
  echo 'Starting server...'; \
  uvicorn app.presentation.api.app:create_app --factory --host 0.0.0.0 --port ${PORT:-8000}"]
