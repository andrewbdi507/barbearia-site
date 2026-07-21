"""Payment Module — Provider Registry.

Registra todos os providers disponíveis no PaymentProviderFactory.
"""

from app.modules.payment.domain.enums import PaymentGateway
from app.modules.payment.domain.interfaces import PaymentProviderFactory
from app.modules.payment.infrastructure.providers.mercado_pago import MercadoPagoProvider
from app.modules.payment.infrastructure.providers.stripe import StripeProvider
from app.modules.payment.infrastructure.providers.asaas import AsaasProvider


def register_providers() -> None:
    """Registra todos os providers no factory.

    Chamado no startup da aplicação.
    """
    PaymentProviderFactory.register(PaymentGateway.MERCADO_PAGO, MercadoPagoProvider)
    PaymentProviderFactory.register(PaymentGateway.STRIPE, StripeProvider)
    PaymentProviderFactory.register(PaymentGateway.ASAAS, AsaasProvider)
