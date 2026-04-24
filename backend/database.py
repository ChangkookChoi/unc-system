import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        dsn = os.environ["DATABASE_URL"].replace("postgresql+asyncpg://", "postgresql://")
        # Supabase는 외부 연결 시 SSL 필요
        ssl = "require" if "supabase.co" in dsn else None
        _pool = await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=5, ssl=ssl)
    return _pool


async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
