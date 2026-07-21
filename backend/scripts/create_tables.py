import os, asyncio
os.environ['DB_HOST'] = 'postgres'
os.environ['DB_PASSWORD'] = 'barbershop_dev'
os.environ['DB_NAME'] = 'barbershop_dev'

from app.core.config import get_settings
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import init_session_factory

import app.modules.tenant.infrastructure.models.tenant_models
import app.modules.auth.infrastructure.models.auth_models
import app.modules.staff.infrastructure.models.staff_models
import app.modules.scheduling.infrastructure.models.scheduling_models
import app.modules.customer.infrastructure.models.customer_models
import app.modules.payment.infrastructure.models.payment_models
import app.modules.notification.infrastructure.models.notification_models
import app.modules.site.infrastructure.models.site_models
import app.modules.analytics.infrastructure.models.analytics_models

s = get_settings()
init_session_factory(s)
from app.infrastructure.database.session import _engine

async def create():
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(f'OK: {len(Base.metadata.tables)} tabelas criadas!')
    for t in sorted(Base.metadata.tables.keys()):
        print(f'  {t}')

asyncio.run(create())
