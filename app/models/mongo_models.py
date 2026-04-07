from datetime import datetime, timezone
from typing import Any

from beanie import Document
from pydantic import Field


class ActivityLog(Document):

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    action_type: str
    user_id: int
    details: dict[str, Any] | None = None

    class Settings:
        # kokoelman nimi (ilman tätä olisi "activitylog")
        name = "activity_logs"