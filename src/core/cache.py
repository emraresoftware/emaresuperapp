"""
Emare SuperApp — Redis Cache Wrapper
"""
from typing import Optional, Any
import json
import logging

logger = logging.getLogger("superapp.cache")

# Redis bağlantısı (lazy init)
_redis = None


async def get_redis():
    """Redis bağlantısını al veya oluştur."""
    global _redis
    if _redis is None:
        try:
            import redis.asyncio as aioredis
            from config.settings import get_settings
            settings = get_settings()
            _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
            logger.info("Redis bağlantısı kuruldu")
        except Exception as e:
            logger.warning(f"Redis bağlantısı kurulamadı: {e}")
            return None
    return _redis


async def cache_get(key: str) -> Optional[Any]:
    """Cache'ten değer oku."""
    r = await get_redis()
    if r is None:
        return None
    val = await r.get(f"superapp:{key}")
    if val:
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            return val
    return None


async def cache_set(key: str, value: Any, ttl: int = 300):
    """Cache'e değer yaz (varsayılan 5 dk)."""
    r = await get_redis()
    if r is None:
        return
    serialized = json.dumps(value) if not isinstance(value, str) else value
    await r.setex(f"superapp:{key}", ttl, serialized)


async def cache_delete(key: str):
    """Cache'ten sil."""
    r = await get_redis()
    if r is None:
        return
    await r.delete(f"superapp:{key}")
