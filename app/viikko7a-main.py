import asyncio
import time

from app.database.sql_db import get_session
from app.database.mongo_db import init_mongo
from app.services import project_service, log_service, cache_service


async def main() -> None:

    await init_mongo()

    with get_session() as session:
        user = project_service.create_user(
            session,
            username="alice2",
            email="alice2@example.com"
        )
        project = project_service.create_project(
            session,
            title="Redis Demo Project",
            owner_id=user.id
        )

        await log_service.create_activity_log(
            action_type="project_created",
            user_id=user.id,
            details={"project_id": project.id, "project_title": project.title}
        )

    # Create activity message
    activity_message = (
        f"User '{user.username}' created project '{project.title}'"
    )

    # ── DEMO 1: Set and Get ──────────────────────────────────
    print("\n--- Demo 1: Set and Get ---")
    cache_service.set_latest_activity(activity_message, ttl=10)  # 10 sec TTL

    # Immediate get - should hit cache
    cached = cache_service.get_latest_activity()
    print(f"Cached value: {cached}")

    # ── DEMO 2: TTL Expiration ───────────────────────────────
    print("\n--- Demo 2: TTL Expiration (waiting 11 seconds) ---")
    print("Waiting for cache to expire...")

    time.sleep(11)  # Wait for TTL to expire

    # Get after expiration - should be None
    cached = cache_service.get_latest_activity()
    print(f"Cached value after expiration: {cached}")

    # ── DEMO 3: Manual Invalidation ──────────────────────────
    print("\n--- Demo 3: Manual Invalidation ---")
    cache_service.set_latest_activity(activity_message, ttl=300)
    print("Cache set with 5 min TTL")

    # Delete manually
    cache_service.delete_latest_activity()

    # Try to get - should be None
    cached = cache_service.get_latest_activity()
    print(f"Cached value after deletion: {cached}")


if __name__ == "__main__":
    asyncio.run(main())