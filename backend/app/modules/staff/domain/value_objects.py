"""Staff Module — Value Objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CommissionRule:
    """Regra de comissão — imutável."""

    commission_type: str  # none, percentage, fixed
    value: int = 0  # percentual (ex: 30 = 30%) ou valor fixo em centavos
    applies_to_all: bool = True
    service_ids: list[str] | None = None  # serviços específicos (se não all)

    def calculate(self, service_price_cents: int) -> int:
        """Calcula comissão para um serviço."""
        if self.commission_type == "none":
            return 0
        if self.commission_type == "percentage":
            return int(service_price_cents * self.value / 100)
        return self.value  # fixed
