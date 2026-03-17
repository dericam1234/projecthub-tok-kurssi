from sqlmodel import Session, select
from app.models.sql_models import User, Project


def create_user(session: Session, username: str, email: str) -> User:
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_project(session: Session, title: str, owner_id: int) -> Project:
    project = Project(title=title, owner_id=owner_id)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def get_user_projects(session: Session, user_id: int) -> list[Project]:
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    # user = session.get(User, user_id)
    if user:
        return user.projects  # Relationship lataa nämä automaattisesti
    return []


def get_user(session: Session, user_id: int) -> User | None:
    user = session.get(User, user_id)
    return user