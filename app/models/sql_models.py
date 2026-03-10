from sqlmodel import SQLModel, Field


class Check(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str
    description: str | None = None