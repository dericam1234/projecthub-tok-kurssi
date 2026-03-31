from datetime import datetime
from sqlmodel import Relationship, SQLModel, Field


class ProjectUserLink(SQLModel, table=True):
    project_id: int | None = Field(
        default=None, foreign_key="project.id", primary_key=True
    )
    user_id: int | None = Field(
        default=None, foreign_key="user.id", primary_key=True
    )

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    username: str = Field(index=True, min_length=3, max_length=20)
    email: str = Field(index=True, min_length=5)

    projects: list["Project"] = Relationship(back_populates="owner")

    member_of_projects: list["Project"] = Relationship(
        back_populates="members",
        link_model=ProjectUserLink
    )


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="projects")

    tasks: list["Task"] = Relationship(back_populates="project")

    members: list[User] = Relationship(
        back_populates="member_of_projects",
        link_model=ProjectUserLink
    )


# Harjoitus, viikko 03
class TaskTagLink(SQLModel, table=True):
    task_id: int | None = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=3)
    status: str = Field(default="todo")

    project_id: int = Field(foreign_key="project.id")
    project: Project = Relationship(back_populates="tasks")

    tags: list["Tag"] = Relationship(
        back_populates="tasks", 
        link_model=TaskTagLink)

    # Viikko 4: Lisää tehtäviin deadline ja priority-kentät
    deadline: datetime | None = Field(default=None)
    priority: int | None = Field(default=None)

class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=30)
    
    tasks: list[Task] = Relationship(
        back_populates="tags", 
        link_model=TaskTagLink)
