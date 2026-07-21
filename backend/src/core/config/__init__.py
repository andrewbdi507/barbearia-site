"""Application configuration — public API.

Exports the canonical get_settings() function and Settings type.
"""

from src.core.config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
