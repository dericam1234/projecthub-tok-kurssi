from sqlmodel import Session, select
from app.models.sql_models import User, Project, Task


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


def create_task(session: Session, name: str, project_id: int, status: str = "todo") -> Task:
    task = Task(name=name, project_id=project_id, status=status)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_project_with_tasks(session: Session, project_id: int) -> Project | None:
    statement = select(Project).where(Project.id == project_id)
    results = session.exec(statement)
    return results.first()


def search_tasks(session: Session, status: str | None = None, keyword: str | None = None) -> list[Task]:
    statement = select(Task)

    if status:
        statement = statement.where(Task.status == status)

    if keyword:
        statement = statement.where(Task.name.contains(keyword))

    statement = statement.order_by(Task.id.desc())

    statement = statement.limit(10)

    return session.exec(statement).all()