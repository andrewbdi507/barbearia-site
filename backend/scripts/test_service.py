import os, asyncio
os.environ['DB_HOST'] = 'postgres'
os.environ['DB_PASSWORD'] = 'barbershop_dev'
os.environ['DB_NAME'] = 'barbershop_dev'

from app.core.config import get_settings
from app.infrastructure.database.session import init_session_factory

s = get_settings()
init_session_factory(s)
from app.infrastructure.database.session import _session_factory

async def test():
    from app.modules.tenant.infrastructure.repository import (
        TenantRepository, PlanRepository, SubscriptionRepository,
        TenantSettingsRepository, TenantBrandingRepository,
        BusinessHoursRepository, DomainRepository,
    )
    from app.modules.tenant.application.tenant_service import TenantService
    from app.infrastructure.cache.null_cache import NullTenantCache

    async with _session_factory() as session:
        service = TenantService(
            tenant_repo=TenantRepository(session),
            plan_repo=PlanRepository(session),
            sub_repo=SubscriptionRepository(session),
            settings_repo=TenantSettingsRepository(session),
            branding_repo=TenantBrandingRepository(session),
            bh_repo=BusinessHoursRepository(session),
            domain_repo=DomainRepository(session),
            cache=NullTenantCache(),
        )
        
        try:
            tenant = await service.create_tenant(
                subdomain='blackhouse2',
                name='Black House Test',
                plan_slug='professional',
            )
            print(f'SUCCESS! Tenant: {tenant.name} (id={tenant.id})')
        except Exception as e:
            print(f'ERROR: {type(e).__name__}: {e}')
            import traceback
            traceback.print_exc()

asyncio.run(test())
