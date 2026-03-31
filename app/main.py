import asyncio

from app.database.sql_db import get_session
#from app.database.sql_db import create_db_and_tables, get_session
from app.services import project_service


async def main() -> None:
    #create_db_and_tables()
    
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
        task1 = project_service.create_task(
            session, "Suunnittele neuroverkko", proj.id, status="doing")
        task2 = project_service.create_task(
            session, "SQL-integraatio", proj.id, status="todo")
        task3 = project_service.create_task(
            session, "Yksikkötestaus", proj.id, status="todo")

        print("\n--- Vaihe 5: Luodaan tageja ---")
        tag1 = project_service.create_tag(session, "Python")
        tag2 = project_service.create_tag(session, "SQL")
        tag3 = project_service.create_tag(session, "Testing")

        # Liitetään tagit tehtäviin
        task1.tags.append(tag1)  # Suunnittele neuroverkko -> Python
        task2.tags.append(tag2)  # SQL-integraatio -> SQL
        task3.tags.append(tag3)  # Yksikkötestaus -> Testing
        session.commit()         # Tallennetaan muutokset tietokantaan
        

        print("\n--- Vaihe 6: Dynaaminen haku ---")
        # Haetaan tehtävät, joiden nimessä on "SQL"
        sql_tasks = project_service.search_tasks(session, keyword="SQL")
        for t in sql_tasks:
            print(f"Löytyi SQL-tehtävä: {t.name} (Status: {t.status})")

        # Haetaan kaikki tehtävät tagilla 'Python' ja näytä tuloksissa tehtävän nimen lisäksi se, mihin projektiin se kuuluu
        python_tasks = project_service.get_tasks_by_tag(session, "Python")
        for t in python_tasks:
            print(f"Löytyi Python-tehtävä: {t.name} (Projektin nimi: {t.project.title})")

if __name__ == "__main__":
    asyncio.run(main())