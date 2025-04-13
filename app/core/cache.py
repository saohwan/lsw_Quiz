from redis import Redis
from app.core.config import settings

redis_client = None


def init_cache():
    global redis_client
    redis_client = Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True
    )
    return redis_client


def get_cache():
    if redis_client is None:
        return init_cache()
    return redis_client


def set_cache(key: str, value: str, expire: int = 60):
    """캐시에 데이터를 저장합니다."""
    return get_cache().set(key, value, ex=expire)


def get_cache_value(key: str) -> str:
    """캐시에서 데이터를 조회합니다."""
    return get_cache().get(key)


def delete_cache(key: str):
    """캐시에서 데이터를 삭제합니다."""
    return get_cache().delete(key)


def clear_cache():
    """모든 캐시를 삭제합니다."""
    return get_cache().flushall() 