import asyncio

from app.database.sql_db import get_session
from app.database.mongo_db import init_mongo
from app.services import project_service, log_service


async def main() -> None:

    await init_mongo()

    user_id = None

    with get_session() as session:
        user = project_service.create_user(
            session,
            username="alice",
            email="alice@example.com"
        )
        print(f"Created user: {user.username} (id={user.id})")

        user_id = user.id

        project = project_service.create_project(
            session,
            title="MyApp Redesign",
            owner_id=user.id
        )
        print(f"Created project: {project.title} (id={project.id})")

    await log_service.create_activity_log(
        action_type="project_created",
        user_id=user_id,
        details={
            "project_id": project.id,
            "project_title": project.title
        }
    )


if __name__ == "__main__":
    asyncio.run(main())