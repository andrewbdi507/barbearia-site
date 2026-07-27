"""Seed do tenant demo — desbloqueia o site público no Render.

Uso:
    cd backend
    python scripts/seed_demo_tenant.py
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import get_settings
from app.infrastructure.database.session import init_session_factory, _session_factory
from app.modules.tenant.infrastructure.models.tenant_models import (
    TenantModel, TenantBrandingModel, BusinessHoursModel, PlanModel,
)
from app.modules.scheduling.infrastructure.models.scheduling_models import (
    ServiceModel, ServiceCategoryModel,
)
from app.modules.staff.infrastructure.models.staff_models import (
    StaffProfileModel, PositionModel,
)
from app.modules.site.infrastructure.models.site_models import (
    SiteContentModel, FAQItemModel,
)
from sqlalchemy import select
from uuid import uuid4


async def seed():
    settings = get_settings()
    init_session_factory(settings)

    async with _session_factory() as session:
        # ---- 1. Encontrar ou criar tenant "demo" ----
        r = await session.execute(
            select(TenantModel).where(TenantModel.subdomain == "demo")
        )
        tenant = r.scalar_one_or_none()

        if tenant is None:
            # Tenta achar qualquer tenant
            r = await session.execute(select(TenantModel).limit(1))
            tenant = r.scalar_one_or_none()

        if tenant is None:
            print("❌ Nenhum tenant encontrado. Execute seed_plans.py primeiro.")
            return

        # Atualiza subdomínio para "demo" (usado pelo fallback do ThemeProvider)
        tenant.subdomain = "demo"
        tenant.name = "Studio 27 Barbearia"
        tenant.slug = "studio-27"
        tenant.address = "Rua Augusta, 1500 — Consolação, São Paulo — SP"
        tenant.phone = "(11) 3120-4567"
        tenant.email = "contato@studio27barber.com.br"
        tenant.whatsapp = "5511999999999"
        tenant.map_embed_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3657.1!2d-46.65!3d-23.55"
        session.add(tenant)
        print(f"✅ Tenant: {tenant.name} (subdomain: demo)")

        # ---- 2. Branding (tema Luxury) ----
        r = await session.execute(
            select(TenantBrandingModel).where(TenantBrandingModel.tenant_id == tenant.id)
        )
        branding = r.scalar_one_or_none()
        if branding is None:
            branding = TenantBrandingModel(id=str(uuid4()), tenant_id=tenant.id)
            session.add(branding)

        branding.theme = "luxury"
        branding.primary_color = "#1a1a1a"
        branding.secondary_color = "#c9a96e"
        branding.background_color = "#fdfbf7"
        branding.surface_color = "#ffffff"
        branding.text_color = "#1a1a1a"
        branding.text_light_color = "#6b6b6b"
        branding.heading_font = "Playfair Display"
        branding.body_font = "Lato"
        branding.border_radius = "4px"
        branding.banner_title = "Studio 27"
        branding.banner_subtitle = "Barbearia premium — tradição e estilo"
        branding.banner_cta_text = "Agende Agora"
        print("✅ Branding: Luxury theme configurado")

        # ---- 3. Horários (Seg-Sáb 08:00-20:00) ----
        r = await session.execute(
            select(BusinessHoursModel).where(BusinessHoursModel.tenant_id == tenant.id)
        )
        existing = r.scalars().all()
        for bh in existing:
            await session.delete(bh)

        for day in range(7):
            is_closed = day == 0  # Domingo fechado
            bh = BusinessHoursModel(
                id=str(uuid4()), tenant_id=tenant.id,
                day_of_week=day, is_closed=is_closed,
                open_time="08:00", close_time="20:00",
                lunch_start="12:00", lunch_end="13:00",
                slot_duration_minutes=30,
            )
            session.add(bh)
        print("✅ Horários: Seg-Sáb 08:00-20:00 (Dom fechado)")

        # ---- 4. Categoria de serviços ----
        r = await session.execute(
            select(ServiceCategoryModel).where(ServiceCategoryModel.tenant_id == tenant.id)
        )
        category = r.scalar_one_or_none()
        if category is None:
            category = ServiceCategoryModel(
                id=str(uuid4()), tenant_id=tenant.id,
                name="Cortes & Barba", color_tag="#c9a96e",
            )
            session.add(category)

        # ---- 5. Serviços ----
        r = await session.execute(
            select(ServiceModel).where(ServiceModel.tenant_id == tenant.id)
        )
        existing_svcs = {s.name: s for s in r.scalars().all()}

        services_data = [
            {"name": "Corte Masculino", "description": "Corte moderno com tesoura e máquina. Inclui lavagem e finalização.", "base_price": 4000, "duration_minutes": 30, "color_tag": "#1a1a1a"},
            {"name": "Barba", "description": "Barba completa com toalha quente, navalha e balm hidratante.", "base_price": 3000, "duration_minutes": 20, "color_tag": "#c9a96e"},
            {"name": "Corte + Barba", "description": "Combo completo: corte masculino + barba com desconto especial.", "base_price": 6000, "duration_minutes": 50, "color_tag": "#8b7355"},
        ]

        for svc in services_data:
            if svc["name"] not in existing_svcs:
                s = ServiceModel(
                    id=str(uuid4()), tenant_id=tenant.id,
                    category_id=category.id,
                    name=svc["name"], description=svc["description"],
                    base_price=svc["base_price"], duration_minutes=svc["duration_minutes"],
                    color_tag=svc["color_tag"], is_active=True,
                )
                session.add(s)
        print(f"✅ Serviços: Corte R$40, Barba R$30, Corte+Barba R$60")

        # ---- 6. Cargo (Position) ----
        r = await session.execute(
            select(PositionModel).where(PositionModel.tenant_id == tenant.id)
        )
        position = r.scalar_one_or_none()
        if position is None:
            position = PositionModel(
                id=str(uuid4()), tenant_id=tenant.id,
                name="Barbeiro", description="Profissional de barbearia",
            )
            session.add(position)

        # ---- 7. Staff ----
        r = await session.execute(
            select(StaffProfileModel).where(StaffProfileModel.tenant_id == tenant.id)
        )
        existing_staff = {s.professional_name: s for s in r.scalars().all()}

        staff_data = [
            {"professional_name": "Marcos Silva", "specialties": ["Cortes modernos", "Degradê"], "experience_years": 8, "bio": "Especialista em cortes modernos e degradê. 8 anos de experiência."},
            {"professional_name": "Ricardo Santos", "specialties": ["Barba", "Hot Towel Shave"], "experience_years": 5, "bio": "Mestre da barba. Toalha quente e navalha com precisão."},
        ]

        for st in staff_data:
            if st["professional_name"] not in existing_staff:
                sp = StaffProfileModel(
                    id=str(uuid4()), tenant_id=tenant.id,
                    user_id=str(uuid4()), position_id=position.id,
                    professional_name=st["professional_name"],
                    specialties=st["specialties"],
                    experience_years=st["experience_years"],
                    bio=st["bio"],
                    status="active", is_visible_on_site=True,
                )
                session.add(sp)
        print("✅ Equipe: Marcos Silva, Ricardo Santos")

        # ---- 8. FAQ ----
        r = await session.execute(
            select(FAQItemModel).where(FAQItemModel.tenant_id == tenant.id)
        )
        existing_faq = r.scalars().all()
        for f in existing_faq:
            await session.delete(f)

        faq_data = [
            ("Preciso agendar ou posso ir direto?", "Recomendamos agendamento online para garantir seu horário, mas aceitamos clientes sem agendamento conforme disponibilidade.", 1),
            ("Quanto tempo dura cada serviço?", "Corte: 30 min. Barba: 20 min. Combo: 50 min.", 2),
            ("Vocês aceitam cartão?", "Sim! Cartão de crédito, débito, Pix e dinheiro.", 3),
            ("Posso cancelar ou reagendar?", "Sim, com até 2h de antecedência pelo link de confirmação.", 4),
            ("Atendem crianças?", "Sim! Temos profissionais especializados em cortes infantis.", 5),
        ]
        for q, a, order in faq_data:
            faq = FAQItemModel(
                id=str(uuid4()), tenant_id=tenant.id,
                question=q, answer=a, sort_order=order,
            )
            session.add(faq)
        print("✅ FAQ: 5 perguntas criadas")

        # ---- 9. Site Content ----
        r = await session.execute(
            select(SiteContentModel).where(SiteContentModel.tenant_id == tenant.id)
        )
        content = r.scalar_one_or_none()
        if content is None:
            content = SiteContentModel(id=str(uuid4()), tenant_id=tenant.id)
            session.add(content)

        content.hero_title = "Estilo & Tradição"
        content.hero_subtitle = "Barbearia premium com agendamento online"
        content.hero_cta_text = "Agendar Horário"
        content.about_title = "Nossa História"
        content.about_text = "Desde 2018, o Studio 27 une o clássico ao contemporâneo. Nossa equipe é treinada nas melhores técnicas — do fade americano ao hot towel shave. Cerveja gelada, whisky selecionado e o melhor café da região aguardam você."
        content.highlights = [
            "Profissionais certificados",
            "Produtos premium importados",
            "Ambiente climatizado",
            "Wi-Fi + bebida cortesia",
        ]
        content.show_services = True
        content.show_team = True
        content.show_reviews = True
        content.show_gallery = True
        print("✅ Site Content: Hero, About, Highlights configurados")

        await session.commit()
        print("\n🎉 Seed concluído! O site deve funcionar em https://agendaos-site.onrender.com")


if __name__ == "__main__":
    asyncio.run(seed())
