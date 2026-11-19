from app.config import app_config
import redis.asyncio as aioredis

redis_client = aioredis.from_url(app_config.REDIS_URL, decode_responses=True)

async def ping_redis() -> bool:
    try:
        return bool(await redis_client.ping())
    except aioredis.RedisError:
        return False

async def close_redis() -> None:
    await redis_client.aclose()