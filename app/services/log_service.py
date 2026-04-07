from app.models.mongo_models import ActivityLog


async def create_activity_log(
    action_type: str,
    user_id: int,
    details: dict | None = None
) -> ActivityLog:
    log = ActivityLog(
        action_type=action_type,
        user_id=user_id,
        details=details
    )
    await log.insert()
    print(f"   [LOG] {action_type} by user {user_id}")
    return log