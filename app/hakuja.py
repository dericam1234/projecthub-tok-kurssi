from datetime import datetime, timedelta, timezone
from beanie.operators import Or

from app.models.mongo_models import ActivityLog


logs = await ActivityLog.find(ActivityLog.user_id == 1).to_list()
logs = await ActivityLog.find(ActivityLog.action_type == "project_created").to_list()

# AND
# Hae alice:n (user_id=1) project_created -lokit
logs = await ActivityLog.find(
    ActivityLog.user_id == 1,
    ActivityLog.action_type == "project_created"
).to_list()


# OR
# Hae lokit jotka ovat JOKO project_created TAI task_created
logs = await ActivityLog.find(
    Or(
        ActivityLog.action_type == "project_created",
        ActivityLog.action_type == "task_created"
    )
).to_list()


# Hae viimeisen tunnin lokit
one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
logs = await ActivityLog.find(
    ActivityLog.timestamp >= one_hour_ago
).to_list()


# Hae lokit tietyllä aikavälillä
start_date = datetime(2025, 2, 10, tzinfo=timezone.utc)
end_date = datetime(2025, 2, 11, tzinfo=timezone.utc)

logs = await ActivityLog.find(
    ActivityLog.timestamp >= start_date,
    ActivityLog.timestamp < end_date
).to_list()

# sort, limit, filter
# Hae alice:n viimeisimmät 5 project-lokia
logs = await ActivityLog.find(
    ActivityLog.user_id == 1,
    ActivityLog.action_type == "project_created"
).sort("-timestamp").limit(5).to_list()

# Järjestys: 1) Suodata, 2) Lajittele, 3) Rajaa


# "Hae alice:n tai bob:n (user_id 1 tai 2)
#  project_created tai task_created -lokit
#  viimeiseltä viikolta,
#  uusin ensin,
#  max 10 kpl"

one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

logs = await ActivityLog.find(
    Or(
        ActivityLog.user_id == 1,
        ActivityLog.user_id == 2
    ),
    Or(
        ActivityLog.action_type == "project_created",
        ActivityLog.action_type == "task_created"
    ),
    ActivityLog.timestamp >= one_week_ago
).sort("-timestamp").limit(10).to_list()