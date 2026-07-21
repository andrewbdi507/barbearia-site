import os, asyncio
os.environ['DB_HOST'] = 'postgres'
os.environ['DB_PASSWORD'] = 'barbershop_dev'
os.environ['DB_NAME'] = 'barbershop_dev'

from app.core.config import get_settings
from app.infrastructure.database.session import init_session_factory

s = get_settings()
init_session_factory(s)
from app.infrastructure.database.session import _session_factory

PLANS = {
    "starter": {
        "price_monthly": 4900,
        "price_yearly": 49000,
        "limits": {"max_staff": 1, "max_customers": 100, "max_bookings_month": 300, "whatsapp": False, "reports": False, "analytics": False},
        "features": ["booking", "customers", "services"],
    },
    "professional": {
        "price_monthly": 9900,
        "price_yearly": 99000,
        "limits": {"max_staff": 5, "max_customers": 0, "max_bookings_month": 0, "whatsapp": True, "reports": True, "analytics": False},
        "features": ["booking", "customers", "services", "staff", "whatsapp", "reports"],
    },
    "premium": {
        "price_monthly": 19900,
        "price_yearly": 199000,
        "limits": {"max_staff": 0, "max_customers": 0, "max_bookings_month": 0, "whatsapp": True, "reports": True, "analytics": True, "priority_support": True},
        "features": ["booking", "customers", "services", "staff", "whatsapp", "reports", "analytics", "priority_support", "automations"],
    },
}

async def seed():
    async with _session_factory() as session:
        import json
        from app.modules.tenant.infrastructure.models.tenant_models import PlanModel
        from sqlalchemy import update

        for slug, data in PLANS.items():
            stmt = (
                update(PlanModel)
                .where(PlanModel.slug == slug)
                .values(
                    price_monthly=data["price_monthly"],
                    price_yearly=data["price_yearly"],
                    limits=data["limits"],
                    features=data["features"],
                )
            )
            await session.execute(stmt)
        await session.commit()
        print("OK: 3 planos atualizados com limites e features")

asyncio.run(seed())
