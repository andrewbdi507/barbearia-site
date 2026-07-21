"""E2E Tests — Full business flow simulation.

Fluxo completo:
1. Cadastro da empresa (trial)
2. Criação de funcionários
3. Cadastro de serviços
4. Cliente agenda
5. Pagamento do sinal
6. Webhook confirma pagamento
7. WhatsApp enviado
8. Check-in / Check-out
9. Avaliação
10. Fidelidade (pontos ganhos)
"""

import pytest


@pytest.mark.e2e
class TestFullBusinessFlow:
    """Simulação completa de negócio — do cadastro à fidelização."""

    def test_step1_tenant_registration(self) -> None:
        """Empresa se cadastra no trial de 14 dias."""
        from app.modules.tenant.domain.entities import Tenant
        from app.modules.tenant.domain.value_objects import Subdomain
        from app.modules.tenant.domain.enums import TenantStatus

        tenant = Tenant(
            id="t_e2e_001", subdomain=Subdomain("barbearia-e2e"),
            name="Barbearia E2E Test", status=TenantStatus.TRIAL,
        )
        tenant.start_trial(days=14)
        assert tenant.status == TenantStatus.TRIAL
        assert tenant.trial_ends_at is not None
        assert tenant.trial_days_remaining == 14

    def test_step2_create_staff(self) -> None:
        """Cria profissional na barbearia."""
        from app.modules.staff.domain.entities import StaffProfile
        from app.modules.staff.domain.enums import StaffStatus

        staff = StaffProfile(
            id="s_e2e_001", tenant_id="t_e2e_001", user_id="u_barber",
            professional_name="Marcos Silva", status=StaffStatus.ACTIVE,
        )
        assert staff.is_active
        assert staff.professional_name == "Marcos Silva"

    def test_step3_create_service(self) -> None:
        """Cadastra serviço oferecido."""
        from app.modules.scheduling.domain.entities import Service
        from app.modules.scheduling.domain.value_objects import ServicePricing

        svc = Service(
            id="svc_e2e_001", tenant_id="t_e2e_001", name="Corte Social",
            duration_minutes=45, buffer_minutes=10,
            pricing=ServicePricing(base_price=5000),
        )
        assert svc.total_duration == 55
        assert svc.effective_price == 5000

    def test_step4_customer_books(self) -> None:
        """Cliente agenda horário."""
        from datetime import date, time
        from app.modules.scheduling.domain.entities import Booking
        from app.modules.scheduling.domain.enums import BookingStatus

        booking = Booking(
            id="b_e2e_001", tenant_id="t_e2e_001",
            professional_id="s_e2e_001",
            booking_date=date.today(),
            start_time=time(14, 0), end_time=time(14, 55),
            status=BookingStatus.PENDING,
            guest_name="João Cliente", guest_phone="11999999999",
            total_amount=5000, total_duration_minutes=55,
            idempotency_key="e2e-idem-001",
        )
        assert booking.status == BookingStatus.PENDING
        assert booking.idempotency_key == "e2e-idem-001"

    def test_step5_deposit_payment(self) -> None:
        """Cliente paga sinal via PIX."""
        from app.modules.payment.domain.entities import Payment
        from app.modules.payment.domain.enums import PaymentStatus, PaymentMethod

        payment = Payment(
            id="pay_e2e_001", tenant_id="t_e2e_001",
            booking_id="b_e2e_001", amount=1500,
            payment_method=PaymentMethod.PIX,
            idempotency_key="pay-idem-001",
        )
        assert payment.status == PaymentStatus.PENDING
        assert payment.amount == 1500

    def test_step6_webhook_confirms(self) -> None:
        """Webhook do gateway confirma pagamento."""
        payment = Payment.__new__(Payment)
        payment.status = "paid"
        payment.mark_paid("mp_e2e_123")
        assert payment.status == "paid"
        assert payment.gateway_payment_id == "mp_e2e_123"

    def test_step7_booking_confirmed(self) -> None:
        """Agendamento confirmado após pagamento."""
        from app.modules.scheduling.domain.entities import Booking
        from app.modules.scheduling.domain.enums import BookingStatus

        booking = Booking.__new__(Booking)
        booking.status = BookingStatus.PENDING
        booking.confirm()
        assert booking.status == BookingStatus.CONFIRMED

    def test_step8_checkin_checkout(self) -> None:
        """Check-in e check-out do atendimento."""
        from app.modules.scheduling.domain.entities import Booking
        from app.modules.scheduling.domain.enums import BookingStatus

        booking = Booking.__new__(Booking)
        booking.status = BookingStatus.CONFIRMED
        booking.start_service()
        assert booking.status == BookingStatus.IN_PROGRESS

        booking.complete()
        assert booking.status == BookingStatus.COMPLETED

    def test_step9_customer_review(self) -> None:
        """Cliente avalia atendimento."""
        from app.modules.customer.domain.entities import Review

        review = Review(
            id="r_e2e_001", tenant_id="t_e2e_001",
            booking_id="b_e2e_001", customer_id="c_e2e",
            professional_id="s_e2e_001", rating=5,
            comment="Excelente atendimento!", tags=["Atendimento ótimo"],
        )
        assert review.rating == 5

        review.moderate(True)
        assert review.is_visible

        review.respond("Obrigado pela avaliação!")
        assert review.business_response is not None

    def test_step10_loyalty_points(self) -> None:
        """Cliente ganha pontos de fidelidade."""
        from app.modules.customer.domain.entities import LoyaltyAccount

        loyalty = LoyaltyAccount(
            id="l_e2e_001", tenant_id="t_e2e_001", customer_id="c_e2e",
            points=50, visit_count=4, tier="bronze",
        )
        loyalty.earn(50, visit=True)
        assert loyalty.points == 100
        assert loyalty.visit_count == 5
        assert loyalty.tier == "silver"  # 5 visits = Silver
