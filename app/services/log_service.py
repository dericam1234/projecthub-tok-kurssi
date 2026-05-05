from app.models.mongo_models import ActivityLog
from datetime import datetime, timezone, timedelta

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

# viikko5
async def get_recent_logs(limit: int = 10) -> list[ActivityLog]:
    logs = await ActivityLog.find().sort("-timestamp").limit(limit).to_list()
    return logs

async def get_logs_by_user(user_id: int) -> list[ActivityLog]:
    logs = await ActivityLog.find({"user_id": user_id}).to_list()
    return logs

async def  get_logs_by_action_type(action_type: str, limit: int = 20) -> list[ActivityLog]:
    logs = await ActivityLog.find({"action_type": action_type}).limit(limit).to_list()
    return logs

# viikko6
async def get_user_activity_summary(
    user_id: int,
    days: int = 7
) -> dict[str, int]:

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    logs = await ActivityLog.find(
        ActivityLog.user_id == user_id,
        ActivityLog.timestamp >= cutoff_date
    ).to_list()

    summary = {}
    for log in logs:
        action = log.action_type
        summary[action] = summary.get(action, 0) + 1

    return summary
  
async def get_action_type_summary() -> list[dict]:
    pipeline = [
        {
            "$group": {
                "_id": "$action_type",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$project": {
                "_id": 0,
                "action_type": "$_id",
                "count": 1
            }
        }
    ]

    result = await ActivityLog.aggregate(pipeline).to_list()
    return result

# viikko6
async def get_logs_by_date_range(start_date: datetime, end_date: datetime) -> list[ActivityLog]:
    logs = await ActivityLog.find(
        ActivityLog.timestamp >= start_date,
        ActivityLog.timestamp <= end_date
    ).to_list()
    return logs

async def get_user_logs_by_action_type(user_id: int, action_type: str) -> list[ActivityLog]:
    logs = await ActivityLog.find(
        ActivityLog.user_id == user_id,
        ActivityLog.action_type == action_type
    ).to_list()
    return logs