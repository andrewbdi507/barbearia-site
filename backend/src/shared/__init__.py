"""Shared utilities.

Cross-cutting utilities that don't belong to any specific layer:
- Type aliases
- Common constants
- Helper functions
"""

from typing import TypeVar

# Generic type for repository pattern
T = TypeVar("T")

# Common type aliases
JsonDict = dict[str, object]
