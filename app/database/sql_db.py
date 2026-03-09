from sqlmodel import create_engine, Session, SQLModel
from app.config import settings

engine = create_engine(settings.postgres_url, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
