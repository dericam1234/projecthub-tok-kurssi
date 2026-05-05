from redis import Redis
from app.config import settings

redis_client = Redis.from_url(
    settings.redis_url,
    decode_responses=True
)


def test_connection() -> bool:
    try:
        redis_client.ping()
        return True
    except Exception as e:
        print(f"Redis connection failed: {e}")
        return False