import pytest
from redis import Redis
from sqlmodel import Session, create_engine, text
from app.config import settings
from pymongo import AsyncMongoClient


def test_postgresql_connection():
    engine = create_engine(settings.postgres_url)
    try:
        with Session(engine) as session:
            result = session.exec(text("SELECT 1")).first()
            assert result[0] == 1
    except Exception as e:
        pytest.fail(f"PostgreSQL-yhteys epäonnistui: {e}")


@pytest.mark.asyncio
async def test_mongodb_connection():
    try:
        client = AsyncMongoClient(settings.mongo_url)
        await client.admin.command('ping')
        assert True
    except Exception as e:
        pytest.fail(f"MongoDB-yhteys epäonnistui: {e}")


def test_redis_connection():
    try:
        r = Redis.from_url(settings.redis_url, decode_responses=True)
        assert r.ping() is True
    except Exception as e:
        pytest.fail(f"Redis-yhteys epäonnistui: {e}")
