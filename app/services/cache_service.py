from app.database.redis_client import redis_client

LATEST_ACTIVITY_KEY = "projecthub:latest_activity"

DEFAULT_TTL = 300


def set_latest_activity(message: str, ttl: int = DEFAULT_TTL) -> None:
    redis_client.set(LATEST_ACTIVITY_KEY, message, ex=ttl)
    print(f"   [CACHE] Stored latest activity (TTL: {ttl}s)")


def get_latest_activity() -> str | None:
    value = redis_client.get(LATEST_ACTIVITY_KEY)
    if value:
        print(f"   [CACHE] Retrieved latest activity from cache")
    else:
        print(f"   [CACHE] Cache miss - key expired or not set")
    return value


def delete_latest_activity() -> None:
    redis_client.delete(LATEST_ACTIVITY_KEY)
    print(f"   [CACHE] Deleted latest activity cache")

# viikko8

def set_user_recent_projects(user_id: int, projects_json: str, ttl: int = 300) -> None:
    key = f"projecthub:user:{user_id}:recent_projects"
    redis_client.set(key, projects_json, ex=ttl)
    print(f"   [CACHE] Stored recent projects for user {user_id} (TTL: {ttl}s)")

def get_user_recent_projects(user_id: int) -> str | None:
    key = f"projecthub:user:{user_id}:recent_projects"
    return redis_client.get(key)
    

def delete_user_recent_projects(user_id: int) -> None:
    key = f"projecthub:user:{user_id}:recent_projects"
    redis_client.delete(key)
    print(f"   [CACHE] Deleted recent projects for user {user_id}")