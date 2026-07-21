# ============================================================
# Barbershop SaaS — Worker Dockerfile
# ============================================================
# Background job processor (notifications, exports, image processing).

FROM python:3.12-slim AS production

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

RUN groupadd -r barbershop && useradd -r -g barbershop -d /app -s /sbin/nologin barbershop

WORKDIR /app

COPY --from=barbershop-backend:latest /app/.venv /app/.venv
COPY --from=barbershop-backend:latest /app /app

RUN chown -R barbershop:barbershop /app

USER barbershop

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=15s \
    CMD curl -f http://localhost:8001/health/live || exit 1

CMD ["/app/.venv/bin/python", "-m", "app.infrastructure.worker.main"]
