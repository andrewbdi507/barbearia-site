import os, asyncio
os.environ['DB_HOST'] = 'postgres'
os.environ['DB_PASSWORD'] = 'barbershop_dev'
os.environ['DB_NAME'] = 'barbershop_dev'

from app.core.config import get_settings
from app.infrastructure.database.session import init_session_factory
from app.modules.auth.infrastructure import security as sec
from uuid import uuid4
from sqlalchemy import text

s = get_settings()
init_session_factory(s)
from app.infrastructure.database.session import _session_factory

async def create_user():
    uid = str(uuid4())
    hashed = sec.hash_password('Admin123!')
    async with _session_factory() as session:
        await session.execute(text(
            "INSERT INTO users (id, email, name, password_hash, is_active, "
            "is_verified, failed_login_attempts, tenant_id, created_at, updated_at) "
            "VALUES (:id, :email, :name, :hash, true, true, 0, :tid, NOW(), NOW())"
        ), {
            'id': uid, 'email': 'admin@blackhouse.com', 'name': 'Joao Silva',
            'hash': hashed, 'tid': 'cb359a53-05a3-4434-b7cd-fa75cb970975'
        })
        await session.commit()
        print(f'OK: admin@blackhouse.com / Admin123!')

asyncio.run(create_user())

asyncio.run(create_user())
