from sqlmodel import Relationship, SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    username: str = Field(index=True, min_length=3, max_length=20)
    email: str = Field(index=True, min_length=5)

    projects: list["Project"] = Relationship(back_populates="owner")


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    owner_id: int = Field(foreign_key="user.id")

    owner: User = Relationship(back_populates="projects")