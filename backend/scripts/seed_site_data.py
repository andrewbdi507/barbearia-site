"""Seed data para o site público — FAQ, conteúdo, contato.

Uso:
    cd backend
    python scripts/seed_site_data.py
"""

import asyncio
import os
import sys

# Adiciona o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import get_settings
from app.infrastructure.database.session import init_session_factory, _session_factory
from app.modules.tenant.infrastructure.repository import TenantRepository
from app.modules.site.infrastructure.repository import (
    FAQRepository,
    SiteContentRepository,
)
from app.modules.site.domain.entities import FAQItem, SiteContent
from uuid import uuid4


FAQ_DATA = [
    {"question": "Preciso agendar ou posso ir direto?", "answer": "Recomendamos o agendamento online para garantir seu horário, mas aceitamos clientes sem agendamento conforme disponibilidade.", "sort_order": 1},
    {"question": "Quanto tempo dura cada serviço?", "answer": "Cada serviço tem uma duração específica, que você pode conferir na página de serviços. Em média, um corte leva 30 minutos e barba 20 minutos.", "sort_order": 2},
    {"question": "Vocês aceitam cartão de crédito?", "answer": "Sim! Aceitamos cartões de crédito, débito, Pix e dinheiro.", "sort_order": 3},
    {"question": "Posso cancelar ou reagendar?", "answer": "Sim, você pode cancelar ou reagendar seu horário pelo link de confirmação que enviamos ou entrando em contato conosco com até 2 horas de antecedência.", "sort_order": 4},
    {"question": "Vocês atendem crianças?", "answer": "Sim! Temos profissionais especializados em cortes infantis. Na hora de agendar, selecione o serviço 'Corte Infantil'.", "sort_order": 5},
    {"question": "Tem estacionamento?", "answer": "Temos convênio com o estacionamento ao lado. Apresente o comprovante de agendamento para obter desconto.", "sort_order": 6},
]

CONTACT_DATA = {
    "address": "Rua Augusta, 1500 - Consolação, São Paulo - SP, 01304-001",
    "phone": "(11) 3120-4567",
    "email": "contato@barbeariaexemplo.com.br",
    "whatsapp": "5511999999999",
    "map_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3657.1!2d-46.65!3d-23.55!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjPCsDMzJzAwLjAiUyA0NsKwMzknMDAuMCJX!5e0!3m2!1spt-BR!2sbr!4v1",
}

SITE_CONTENT_DATA = {
    "hero_title": "Tradição e Estilo",
    "hero_subtitle": "Barbearia premium com agendamento online — seu visual em boas mãos",
    "hero_cta_text": "Agendar Horário",
    "about_title": "Nossa História",
    "about_text": "Desde 2018, a Barbearia Exemplo une o clássico ao contemporâneo. Nossa equipe de barbeiros é treinada nas melhores técnicas — do fade americano ao hot towel shave. Aqui, cada cliente recebe atendimento personalizado em um ambiente pensado para o seu conforto. Cerveja gelada, whisky selecionado e o melhor café da região aguardam você.",
    "highlights": [
        "Profissionais certificados internacionalmente",
        "Produtos premium importados",
        "Ambiente climatizado com música ao vivo",
        "Wi-Fi gratuito e bebida cortesia",
    ],
    "show_services": True,
    "show_team": True,
    "show_reviews": True,
    "show_gallery": True,
}


async def seed():
    settings = get_settings()
    init_session_factory(settings)

    async with _session_factory() as session:
        tenant_repo = TenantRepository(session)
        faq_repo = FAQRepository(session)
        content_repo = SiteContentRepository(session)

        # Find the demo/first tenant
        tenant = await tenant_repo.get_by_subdomain("demo")
        if tenant is None:
            # Try to find any tenant
            from sqlalchemy import select
            from app.modules.tenant.infrastructure.models.tenant_models import TenantModel
            r = await session.execute(select(TenantModel).limit(1))
            tenant = r.scalar_one_or_none()

        if tenant is None:
            print("Nenhum tenant encontrado. Execute seed_plans.py e crie um tenant primeiro.")
            return

        tid = tenant.id
        print(f"Tenant: {tenant.name} ({tenant.subdomain if hasattr(tenant.subdomain, 'value') else tenant.subdomain})")

        # ---- Contact info ----
        tenant.address = CONTACT_DATA["address"]
        tenant.phone = CONTACT_DATA["phone"]
        tenant.email = CONTACT_DATA["email"]
        tenant.whatsapp = CONTACT_DATA["whatsapp"]
        tenant.map_embed_url = CONTACT_DATA["map_embed_url"]
        session.add(tenant)
        print("✅ Contato atualizado")

        # ---- FAQ ----
        existing = await faq_repo.list_for_tenant(tid)
        for f in existing:
            await faq_repo.delete(f.id)

        for item in FAQ_DATA:
            faq = FAQItem(
                id=str(uuid4()),
                tenant_id=tid,
                question=item["question"],
                answer=item["answer"],
                sort_order=item["sort_order"],
            )
            await faq_repo.upsert(faq)
        print(f"✅ {len(FAQ_DATA)} FAQs criadas")

        # ---- Site Content ----
        content = SiteContent(
            id=str(uuid4()),
            tenant_id=tid,
            hero_title=SITE_CONTENT_DATA["hero_title"],
            hero_subtitle=SITE_CONTENT_DATA["hero_subtitle"],
            hero_cta_text=SITE_CONTENT_DATA["hero_cta_text"],
            about_title=SITE_CONTENT_DATA["about_title"],
            about_text=SITE_CONTENT_DATA["about_text"],
            highlights=SITE_CONTENT_DATA["highlights"],
            show_services=SITE_CONTENT_DATA["show_services"],
            show_team=SITE_CONTENT_DATA["show_team"],
            show_reviews=SITE_CONTENT_DATA["show_reviews"],
            show_gallery=SITE_CONTENT_DATA["show_gallery"],
        )
        await content_repo.upsert(content)
        print("✅ Conteúdo do site atualizado")

        await session.commit()
        print("\n🎉 Seed concluído!")


if __name__ == "__main__":
    asyncio.run(seed())
