import os, asyncio
os.environ['DB_HOST'] = 'postgres'
os.environ['DB_PASSWORD'] = 'barbershop_dev'
os.environ['DB_NAME'] = 'barbershop_dev'

from app.core.config import get_settings
from app.infrastructure.database.session import init_session_factory
from sqlalchemy import select
from uuid import uuid4
from datetime import datetime, timezone

s = get_settings()
init_session_factory(s)
from app.infrastructure.database.session import _session_factory

async def test():
    from app.modules.tenant.infrastructure.models.tenant_models import TenantModel
    
    async with _session_factory() as session:
        # Create tenant via ORM
        tid = str(uuid4())
        tenant = TenantModel(
            id=tid,
            subdomain='test-orm',
            name='Test ORM',
            slug='test-orm',
            status='trial',
            extra_data={},
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(tenant)
        await session.flush()
        print(f'Flushed tenant: {tid}')
        
        # Query it back
        result = await session.execute(
            select(TenantModel).where(TenantModel.id == tid)
        )
        found = result.scalar_one()
        print(f'Found: {found.name} ({found.subdomain})')
        
        await session.commit()
        print('Committed!')

asyncio.run(test())
