# ============================================================
# Barbershop SaaS — Multi-stage Dockerfile (Backend)
# ============================================================
# Targets: base, development, production
# Size target: < 200 MB (production)

# ---- Stage 0: Base ----
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_COMPILE_BYTECODE=1

# Install only essential system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

# ---- Stage 1: Development ----
FROM base AS development

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* README.md ./
RUN uv sync --dev

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
    CMD curl -f http://localhost:8000/health/live || exit 1

CMD ["uv", "run", "uvicorn", "app.presentation.api.app:create_app", \
     "--factory", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---- Stage 2: Builder (compiles .pyc, strips dev deps) ----
FROM base AS builder

COPY pyproject.toml uv.lock* README.md ./
RUN uv sync --no-dev

COPY . .

# ---- Stage 3: Production (non-root, minimal) ----
FROM python:3.12-slim AS production

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r barbershop && useradd -r -g barbershop -d /app -s /sbin/nologin barbershop

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

RUN chown -R barbershop:barbershop /app

USER barbershop

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=15s \
    CMD curl -f http://localhost:8000/health/live || exit 1

CMD ["/app/.venv/bin/uvicorn", "app.presentation.api.app:create_app", \
     "--factory", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "4"]
