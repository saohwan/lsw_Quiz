from typing import Any, Optional
import json
from redis import Redis
from app.core.config import settings

redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_from_cache(key: str) -> Optional[Any]:
    """캐시에서 데이터를 가져옵니다."""
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


async def set_to_cache(key: str, value: Any, expire: int = 3600) -> None:
    """데이터를 캐시에 저장합니다."""
    redis_client.setex(key, expire, json.dumps(value))


async def delete_from_cache(key: str) -> None:
    """캐시에서 데이터를 삭제합니다."""
    redis_client.delete(key)


async def clear_cache() -> None:
    """모든 캐시를 삭제합니다."""
    redis_client.flushdb()


async def init_cache() -> None:
    """캐시 초기화 함수입니다."""
    # Redis 연결 테스트
    try:
        redis_client.ping()
    except Exception as e:
        print(f"Redis 연결 실패: {e}")
        raise e 