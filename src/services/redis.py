import asyncio

from redis.asyncio import Redis, ConnectionPool

from core.config import redis_config

redis_pool: ConnectionPool = ConnectionPool.from_url(
    redis_config.redis_url,
    decode_responses=redis_config.decode_responses,
    max_connections=redis_config.max_connections
)
redis_semaphore = asyncio.Semaphore(redis_config.max_connections)


async def get_redis() -> Redis:
    await redis_semaphore.acquire()
    try:
        return Redis(connection_pool=redis_pool)
    finally:
        redis_semaphore.release()
        
