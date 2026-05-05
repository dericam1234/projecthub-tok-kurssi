import asyncio

from app.database.sql_db import get_session
from app.database.mongo_db import init_mongo
from app.services import project_service, log_service


async def main() -> None:

    await init_mongo()

    with get_session() as session:

        #--- luodaan käyttäjä 1 ja projekti 1 sekä kirjataan logiin ---
        user1 = project_service.create_user(
            session,
            username="cassandra",
            email="cassandra@example.com"
        )
        print(f"Created user: {user1.username} (id={user1.id})")

        user_id1 = user1.id

        u1_details = {
            "username": user1.username,
            "email": user1.email
        }

        await log_service.create_activity_log(
        action_type="user_registered",
        user_id=user_id1,
        details=u1_details
        )

        #luodaan projekti 1
        project1 = project_service.create_project(
            session,
            title="MyApp Redesign",
            owner_id=user1.id
        )
        print(f"Created project: {project1.title} (id={project1.id})")

        p1_details = {
            "project_id": project1.id,
            "project_title": project1.title
        }

        await log_service.create_activity_log(
        action_type="project_created",
        user_id=user_id1,
        details=p1_details
        )



        #--- luodaan käyttäjä 2 ja projekti 2 sekä kirjataan logiin ---
        user2 = project_service.create_user(
            session,
            username="bob",
            email="bob@example.com"
        )
        print(f"Created user: {user2.username} (id={user2.id})")

        user_id2 = user2.id

        u2_details = {
            "username": user2.username,
            "email": user2.email
        }

        await log_service.create_activity_log(
        action_type="user_registered",
        user_id=user_id2,
        details=u2_details
        )
        

        #luodaan projekti 2
        project2 = project_service.create_project(
            session,
            title="Bob's App Redesign",
            owner_id=user2.id
        )
        print(f"Created project: {project2.title} (id={project2.id})")

        p2_details = {
            "project_id": project2.id,
            "project_title": project2.title
        }

        await log_service.create_activity_log(
        action_type="project_created",
        user_id=user_id2,
        details=p2_details
        )

        #--- luodaan tehtävät ja kirjataan logiin ---
        task1 = project_service.create_task(
            session,
            name="Design new UI",
            project_id=project1.id)
        print(f"Created task: {task1.name} (id={task1.id})")

        t1_details = {
            "task_id": task1.id,
            "task_name": task1.name
        }
         
        await log_service.create_activity_log(
            action_type="task_created",
            user_id=user_id1,
            details=t1_details
        )


    #haetaan logit ja tulostetaan ne konsoliin
    print("--- Recent Activity (last 10) ---")
    recent_logs = await log_service.get_recent_logs()
    for log in recent_logs:
        print(f"[{log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {log.action_type} by user {log.user_id}")

    print(f"--- All actions by user {user_id1} ---")
    user_logs = await log_service.get_logs_by_user(user_id1)
    for log in user_logs:
        print(f"[{log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {log.action_type} by user {log.user_id}")



if __name__ == "__main__":
    asyncio.run(main())