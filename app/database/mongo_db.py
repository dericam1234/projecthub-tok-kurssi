from pymongo import AsyncMongoClient
from beanie import init_beanie

from app.config import settings
from app.models.mongo_models import ActivityLog


async def init_mongo() -> None:
    client = AsyncMongoClient(settings.mongo_url)
    database = client[settings.mongo_db_name]

    await init_beanie(
        database=database,
        document_models=[ActivityLog],
    )
    # print(f"Connected to MongoDB: {settings.mongo_db_name}")