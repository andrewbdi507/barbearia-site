# ============================================================
# Barbershop SaaS — Scheduler Dockerfile
# ============================================================
# Scheduled tasks: cleanup, analytics aggregation, backup trigger.

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

HEALTHCHECK --interval=60s --timeout=5s --retries=3 --start-period=30s \
    CMD curl -f http://localhost:8002/health/live || exit 1

CMD ["/app/.venv/bin/python", "-m", "app.infrastructure.scheduler.main"]
