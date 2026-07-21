"""Payment Module — Provider Interface (ABC).

Provider Pattern: o sistema NUNCA conhece o gateway.
Para adicionar um novo gateway, basta implementar esta interface.

Exemplo:
    PaymentProvider
    ├── MercadoPagoProvider
    ├── StripeProvider
    ├── AsaasProvider
    └── PagSeguroProvider
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.modules.payment.domain.entities import Payment


class PaymentProvider(ABC):
    """Interface abstrata para gateway de pagamento.

    Cada provedor implementa:
    - create_payment: Cria cobrança (PIX, cartão, boleto)
    - get_payment: Consulta status
    - cancel_payment: Cancela cobrança pendente
    - refund_payment: Reembolsa pagamento
    - verify_webhook_signature: Valida assinatura do webhook
    - parse_webhook: Converte payload bruto em evento padronizado
    """

    @abstractmethod
    async def create_payment(
        self, payment: Payment, **kwargs: Any,
    ) -> dict[str, Any]:
        """Cria cobrança no gateway.

        Returns:
            {
                "gateway_payment_id": "mp_123",
                "status": "pending",
                "pix_qr_code": "...",      # PIX
                "pix_copy_paste": "...",   # PIX
                "pix_expires_at": "...",   # PIX
                "checkout_url": "...",     # Cartão
                "boleto_url": "...",       # Boleto
                "boleto_barcode": "...",   # Boleto
                "raw_response": {...},     # Completo (para event sourcing)
            }
        """
        ...

    @abstractmethod
    async def get_payment(self, gateway_payment_id: str) -> dict[str, Any]:
        """Consulta status de pagamento no gateway."""
        ...

    @abstractmethod
    async def cancel_payment(self, gateway_payment_id: str) -> dict[str, Any]:
        """Cancela cobrança pendente no gateway."""
        ...

    @abstractmethod
    async def refund_payment(
        self, gateway_payment_id: str, amount: int | None = None,
    ) -> dict[str, Any]:
        """Reembolsa pagamento (total ou parcial)."""
        ...

    @abstractmethod
    def verify_webhook_signature(
        self, payload: bytes, signature: str, secret: str,
    ) -> bool:
        """Verifica assinatura do webhook — anti-spoofing."""
        ...

    @abstractmethod
    def parse_webhook(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Converte payload bruto do gateway em formato padronizado.

        Returns:
            {
                "gateway_event_id": "evt_123",
                "gateway_payment_id": "mp_456",
                "status": "paid",
                "amount": 4500,
                "raw_data": {...},
            }
        """
        ...


class PaymentProviderFactory:
    """Factory que retorna o provider correto baseado no gateway."""

    _providers: dict[str, type[PaymentProvider]] = {}

    @classmethod
    def register(cls, gateway: str, provider_class: type[PaymentProvider]) -> None:
        cls._providers[gateway] = provider_class

    @classmethod
    def create(cls, gateway: str, **deps: Any) -> PaymentProvider:
        provider_class = cls._providers.get(gateway)
        if provider_class is None:
            raise ValueError(f"Gateway '{gateway}' não registrado.")
        return provider_class(**deps)
