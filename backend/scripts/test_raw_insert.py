import os, asyncio
os.environ['DB_HOST'] = 'postgres'
os.environ['DB_PASSWORD'] = 'barbershop_dev'
os.environ['DB_NAME'] = 'barbershop_dev'

from app.core.config import get_settings
from app.infrastructure.database.session import init_session_factory
from sqlalchemy import text, select, func
from uuid import uuid4

s = get_settings()
init_session_factory(s)
from app.infrastructure.database.session import _session_factory

async def test():
    from app.modules.tenant.infrastructure.models.tenant_models import TenantModel
    
    async with _session_factory() as session:
        # Count tenants
        result = await session.execute(select(func.count()).select_from(TenantModel))
        count = result.scalar()
        print(f'Tenants before: {count}')
        
        # Insert raw
        tid = str(uuid4())
        await session.execute(text(
            f"INSERT INTO tenants (id, subdomain, name, slug, status, extra_data, created_at, updated_at) "
            f"VALUES ('{tid}', 'test123', 'Test', 'test123', 'trial', '{{}}', NOW(), NOW())"
        ))
        await session.commit()
        print(f'Created: {tid}')
        
        # Verify
        result = await session.execute(select(func.count()).select_from(TenantModel))
        print(f'Tenants after: {result.scalar()}')

asyncio.run(test())
