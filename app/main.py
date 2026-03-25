import asyncio

from app.database.sql_db import create_db_and_tables, get_session
from app.services import project_service


async def main() -> None:
    create_db_and_tables()

    with get_session() as session:
        print("\n--- Vaihe 2: Luodaan käyttäjiä ---")
        u1 = project_service.create_user(
            session, "liisa_arkkitehti", "liisa@hub.fi")
        u2 = project_service.create_user(session, "matti_dev", "matti@hub.fi")
        u3 = project_service.create_user(
            session, "tiina_tester", "tiina@hub.fi")

        print("\n--- Vaihe 3: Luodaan projekti ja lisätään jäseniä (M:M) ---")
        proj = project_service.create_project(
            session, "Salainen AI-projekti", u1.id)

        proj.members.append(u2)
        proj.members.append(u3)
        session.add(proj)
        session.commit()
        session.refresh(proj)

        print(f"Projekti '{proj.title}' luotu.")
        print(f"Omistaja: {proj.owner.username}")
        print(f"Jäsenet: {[m.username for m in proj.members]}")

        print("\n--- Vaihe 4: Luodaan tehtäviä hakuja varten ---")
        project_service.create_task(
            session, "Suunnittele neuroverkko", proj.id, status="doing")
        project_service.create_task(
            session, "SQL-integraatio", proj.id, status="todo")
        project_service.create_task(
            session, "Yksikkötestaus", proj.id, status="todo")

        print("\n--- Vaihe 5: Dynaaminen haku ---")
        # Haetaan tehtävät, joiden nimessä on "SQL"
        sql_tasks = project_service.search_tasks(session, keyword="SQL")
        for t in sql_tasks:
            print(f"Löytyi SQL-tehtävä: {t.name} (Status: {t.status})")


if __name__ == "__main__":
    asyncio.run(main())