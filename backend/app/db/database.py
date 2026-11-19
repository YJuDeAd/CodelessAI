from app.config import BASE_DIR, app_config
from app.db.schema import create_schema
import aiosqlite

DB_URL = str((BASE_DIR / app_config.DATABASE_URL).resolve())

async def get_db_connection():
    async with aiosqlite.connect(DB_URL) as conn:
        conn.row_factory = aiosqlite.Row
        await conn.execute("PRAGMA foreign_keys = ON")
        await conn.execute("PRAGMA journal_mode = WAL")
        yield conn

async def init_db():
    async with aiosqlite.connect(DB_URL) as conn:
        await conn.execute("PRAGMA journal_mode = WAL")
        cursor = await conn.cursor()
        await create_schema(cursor)
        await conn.commit()

async def check_db_health():
    try:
        async with aiosqlite.connect(DB_URL) as conn:
            await conn.execute("SELECT 1")
        return True
    except:
        return False