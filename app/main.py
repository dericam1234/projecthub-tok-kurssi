import asyncio

from app.database.sql_db import create_db_and_tables, get_session
from app.services import project_service


async def main() -> None:
    create_db_and_tables()

    with get_session() as session:
        # user = project_service.create_user(
        #     session, "teemu_koodari", "teemu@amk.fi")

        user = project_service.get_user(session, 1)
        if user:
            p = project_service.create_project(
                session, "Tietokantakurssi 2026 2", user.id)

            # user_projects = project_service.get_user_projects(session, user.id)
            # print(user_projects)

            print(
                f"Käyttäjällä {user.username} on projektit: {[proj.title for proj in user.projects]}")


if __name__ == "__main__":
    asyncio.run(main())