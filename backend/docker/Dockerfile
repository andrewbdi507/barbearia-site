# Barbershop SaaS — Dockerfile (Multi-stage)
# ============================================================

# ---- Base Stage ----
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
RUN pip install uv

WORKDIR /app

# ---- Development Stage ----
FROM base AS development

# Install dev dependencies
COPY pyproject.toml uv.lock* ./
RUN uv sync --dev

# Copy source code (mounted as volume in docker-compose)
COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/live || exit 1

CMD ["uv", "run", "uvicorn", "src.presentation.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---- Production Stage ----
FROM base AS production

# Install only production dependencies
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev

# Copy source code
COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/live || exit 1

# Run with multiple workers (production)
CMD ["uv", "run", "uvicorn", "src.presentation.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
