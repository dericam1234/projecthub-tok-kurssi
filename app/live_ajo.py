import asyncio
from datetime import datetime, timedelta

from sqlmodel import select

from app.database.sql_db import get_session
from app.services import project_service
from app.models.sql_models import Task


async def main() -> None:
    
    with get_session() as session:
        print("\n--- Vaihe 1: Luodaan käyttäjiä ---")
        u1 = project_service.create_user(
            session, "liisa_arkkitehti", "liisa@hub.fi")
        u2 = project_service.create_user(session, "matti_dev", "matti@hub.fi")
        u3 = project_service.create_user(
            session, "tiina_tester", "tiina@hub.fi")

        print("\n--- Vaihe 2: Luodaan projekti ja lisätään jäseniä (M:M) ---")
        proj = project_service.create_project(
            session, "Salainen AI-projekti", u1.id, is_active=True)

        proj.members.append(u2)
        proj.members.append(u3)
        session.add(proj)
        session.commit()
        session.refresh(proj)

        print(f"Projekti '{proj.title}' luotu (Aktiivinen: {proj.is_active}).")
        print(f"Omistaja: {proj.owner.username}")
        print(f"Jäsenet: {[m.username for m in proj.members]}")

        print("\n--- Vaihe 3: Luodaan tehtäviä hakuja varten (sis. priority & deadline) ---")
        task1 = project_service.create_task(
            session, "Suunnittele neuroverkko", proj.id, status="doing",
            priority=10, deadline=datetime.now() + timedelta(days=10))
        task2 = project_service.create_task(
            session, "SQL-integraatio", proj.id, status="todo",
            priority=5, deadline=datetime.now() + timedelta(days=20))
        task3 = project_service.create_task(
            session, "Yksikkötestaus", proj.id, status="todo",
            priority=8, deadline=datetime.now() - timedelta(days=1)) # Deadline mennyt

        print(f"Tehtävä luotu: {task1.name}, Prioriteetti: {task1.priority}, Deadline: {task1.deadline.strftime('%Y-%m-%d')}")
        print(f"Tehtävä luotu: {task2.name}, Prioriteetti: {task2.priority}, Deadline: {task2.deadline.strftime('%Y-%m-%d')}")
        print(f"Tehtävä luotu: {task3.name}, Prioriteetti: {task3.priority}, Deadline: {task3.deadline.strftime('%Y-%m-%d')}")


        print("\n--- Vaihe 4: Luodaan tageja ---")
        tag1 = project_service.create_tag(session, "Python")
        tag2 = project_service.create_tag(session, "SQL")
        tag3 = project_service.create_tag(session, "Testing")

        # Liitetään tagit tehtäviin
        task1.tags.append(tag1)  # Suunnittele neuroverkko -> Python
        task2.tags.append(tag2)  # SQL-integraatio -> SQL
        task3.tags.append(tag3)  # Yksikkötestaus -> Testing
        session.commit()         # Tallennetaan muutokset tietokantaan
        

        print("\n--- Vaihe 5: Dynaaminen haku ---")
        # Haetaan tehtävät, joiden nimessä on "SQL"
        sql_tasks = project_service.search_tasks(session, keyword="SQL")
        for t in sql_tasks:
            print(f"Löytyi SQL-tehtävä: {t.name} (Status: {t.status})")

        # Haetaan kaikki tehtävät tagilla 'Python' ja näytä tuloksissa tehtävän nimen lisäksi se, mihin projektiin se kuuluu
        python_tasks = project_service.get_tasks_by_tag(session, "Python")
        for t in python_tasks:
            print(f"Löytyi Python-tehtävä: {t.name} (Projektin nimi: {t.project.title})")

        print("\n--- Vaihe 6: Uudet haut (priority & deadline) ---")
        
        # Haku 1: Hae korkean prioriteetin tehtävät (priority > 5)
        print("\nHaetaan korkean prioriteetin (priority > 5) tehtävät:")
        high_prio_statement = select(Task).where(Task.priority > 5)
        high_prio_tasks = session.exec(high_prio_statement).all()
        for t in high_prio_tasks:
            print(f"Löytyi korkean prioriteetin tehtävä: {t.name} (Priority: {t.priority})")

        # Haku 2: Hae tehtävät, joiden deadline on tulevaisuudessa
        print("\nHaetaan tulevaisuudessa erääntyvät tehtävät:")
        future_tasks_statement = select(Task).where(Task.deadline > datetime.now())
        future_tasks = session.exec(future_tasks_statement).all()
        for t in future_tasks:
            print(f"Löytyi tuleva tehtävä: {t.name} (Deadline: {t.deadline.strftime('%Y-%m-%d')})")


if __name__ == "__main__":
    asyncio.run(main())
