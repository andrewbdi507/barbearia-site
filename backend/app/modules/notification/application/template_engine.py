"""Notification Module — Template Engine.

Resolve templates com variáveis: {{customer.name}}, {{booking.date}}, etc.
"""

from __future__ import annotations

import re
from typing import Any


class TemplateEngine:
    """Motor de renderização de templates.

    Substitui {{variavel}} por valores do payload.
    Suporta acesso aninhado: {{customer.name}}, {{company.logo_url}}.
    """

    VAR_PATTERN = re.compile(r"\{\{\s*([\w.]+)\s*\}\}")

    @classmethod
    def render(cls, template: str, payload: dict[str, Any]) -> str:
        """Renderiza template com payload.

        Exemplo:
            template = "Olá {{customer.name}}, seu horário é {{booking.time}}"
            payload = {"customer": {"name": "João"}, "booking": {"time": "14:30"}}
            result = "Olá João, seu horário é 14:30"
        """

        def resolve(path: str) -> str:
            parts = path.split(".")
            value: Any = payload
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part, "")
                else:
                    return ""
            return str(value) if value is not None else ""

        return cls.VAR_PATTERN.sub(lambda m: resolve(m.group(1)), template)

    @classmethod
    def extract_variables(cls, template: str) -> list[str]:
        """Extrai todas as variáveis usadas no template."""
        return list(set(m.group(1) for m in cls.VAR_PATTERN.finditer(template)))

    @classmethod
    def validate(cls, template: str, payload: dict[str, Any]) -> tuple[bool, list[str]]:
        """Valida se todas as variáveis do template estão presentes no payload."""
        variables = cls.extract_variables(template)
        missing: list[str] = []

        def check_exists(path: str) -> bool:
            parts = path.split(".")
            value: Any = payload
            for part in parts:
                if isinstance(value, dict):
                    if part not in value:
                        return False
                    value = value[part]
                else:
                    return False
            return True

        for var in variables:
            if not check_exists(var):
                missing.append(var)

        return len(missing) == 0, missing
