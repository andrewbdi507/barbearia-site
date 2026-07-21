"""Infrastructure — Adaptadores concretos.

database/    → SQLAlchemy engine, session, base model
cache/       → Redis client
http/        → HTTP client (httpx)
events/      → Event bus (Redis Streams)
workers/     → Background workers
repositories/→ Implementações concretas dos repositórios
security/    → Implementações de segurança
"""
