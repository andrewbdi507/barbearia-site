"""Presentation Layer.

The presentation layer handles HTTP concerns:
- FastAPI application factory
- Route registration
- Middleware (CORS, security headers, rate limiting, request ID)
- Error handlers (RFC 7807 Problem Details)
- API schemas (Pydantic models for request/response)
"""
