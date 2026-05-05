import asyncio
from datetime import datetime, timedelta, timezone
from beanie.operators import Or
import json

from app.database.sql_db import get_session
from app.database.mongo_db import init_mongo
from app.models.mongo_models import ActivityLog
from app.services import project_service, log_service, cache_service


async def main() -> None:
    print("Alustetaan MongoDB-yhteys...")
    await init_mongo()

    now = datetime.now(timezone.utc)

    print("\n--- Vaihe 0: Luodaan oikeat PostgreSQL-tiedot ja MongoDB-logit ---")
    print("\n--- Vaihe 1: Luodaan oikeat PostgreSQL-tiedot ja MongoDB-logit ---")
    with get_session() as session:
        # Luodaan uniikit käyttäjät timestampin avulla, jottei tule PostgreSQL unique-virheitä
        ts = int(now.timestamp())
        user1 = project_service.create_user(session, username=f"alice_{ts}", email=f"alice{ts}@hub.fi")
        user2 = project_service.create_user(session, username=f"bob_{ts}", email=f"bob{ts}@hub.fi")
        print(f"Luotiin PG-käyttäjät: {user1.username} (ID: {user1.id}) ja {user2.username} (ID: {user2.id})")

        # Logitetaan rekisteröitymiset
        await log_service.create_activity_log("user_registered", user1.id, {"username": user1.username})
        await log_service.create_activity_log("user_registered", user2.id, {"username": user2.username})

        # Luodaan projektit
        proj1 = project_service.create_project(session, title=f"Alicen projekti {ts}", owner_id=user1.id)
        proj2 = project_service.create_project(session, title=f"Bobin projekti {ts}", owner_id=user2.id)
        
        # Logitetaan projektit
        await log_service.create_activity_log("project_created", user1.id, {"project_id": proj1.id})
        await log_service.create_activity_log("project_created", user2.id, {"project_id": proj2.id})

        # Luodaan tehtävät
        task1 = project_service.create_task(session, name="Tee koodit", project_id=proj1.id)
        task2 = project_service.create_task(session, name="Testaa koodit", project_id=proj2.id)

        # Logitetaan tehtävät
        await log_service.create_activity_log("task_created", user1.id, {"task_id": task1.id})
        await log_service.create_activity_log("task_created", user2.id, {"task_id": task2.id})

    print("\n--- Vaihe 0.5: Testataan Redis-välimuistia (Cache hit & miss) ---")
    print("\n--- Vaihe 2: Testataan Redis-välimuistia (Cache hit & miss) ---")
    cache_msg = f"Käyttäjä {user1.username} lisäsi juuri dataa järjestelmään."
    cache_service.set_latest_activity(cache_msg, ttl=60)
    cached_val = cache_service.get_latest_activity()
    print(f"Cache HIT: Tallennettiin ja haettiin Rediksestä: '{cached_val}'")

    cache_service.delete_latest_activity()
    miss_val = cache_service.get_latest_activity()
    print(f"Cache MISS: Poiston jälkeen Rediksestä haettu arvo on: '{miss_val}'")

    print(f"\n--- 0. Perushaut (Käyttäjä {user1.username} ja 'project_created' erikseen) ---")
    print(f"\n--- Haku 1: Perushaut (Käyttäjä {user1.username} ja 'project_created' erikseen) ---")
    basic_logs_1 = await ActivityLog.find(ActivityLog.user_id == user1.id).to_list()
    print(f"Löytyi {len(basic_logs_1)} lokia käyttäjältä {user1.id} ({user1.username}).")
    
    basic_logs_2 = await ActivityLog.find(ActivityLog.action_type == "project_created").to_list()
    print(f"Löytyi {len(basic_logs_2)} 'project_created' -lokia kaikilta käyttäjiltä.")

    print(f"\n--- 1. Hae {user1.username}:n (user_id={user1.id}) project_created -lokit ---")
    print(f"\n--- Haku 2: Hae {user1.username}:n (user_id={user1.id}) project_created -lokit ---")
    logs1 = await ActivityLog.find(
        ActivityLog.user_id == user1.id,
        ActivityLog.action_type == "project_created"
    ).to_list()
    for log in logs1:
        print(f"[{log.timestamp}] User {log.user_id}: {log.action_type}")

    print(f"\n--- 2. Hae lokit jotka ovat JOKO project_created TAI task_created ---")
    print(f"\n--- Haku 3: Hae lokit jotka ovat JOKO project_created TAI task_created ---")
    logs2 = await ActivityLog.find(
        Or(
            ActivityLog.action_type == "project_created",
            ActivityLog.action_type == "task_created"
        )
    ).limit(5).to_list() # Rajoitetaan tulostusta jos kanta on suuri
    for log in logs2:
        print(f"[{log.timestamp}] User {log.user_id}: {log.action_type}")

    print("\n--- 3. Hae viimeisen tunnin lokit ---")
    print("\n--- Haku 4: Hae viimeisen tunnin lokit ---")
    one_hour_ago = now - timedelta(hours=1)
    logs3 = await ActivityLog.find(
        ActivityLog.timestamp >= one_hour_ago
    ).limit(5).to_list()
    for log in logs3:
        print(f"[{log.timestamp}] User {log.user_id}: {log.action_type}")

    print("\n--- 4. Hae lokit tietyllä aikavälillä ---")
    print("\n--- Haku 5: Hae lokit tietyllä aikavälillä ---")
    start_date = now - timedelta(days=3)
    end_date = now + timedelta(days=1)
    logs4 = await ActivityLog.find(
        ActivityLog.timestamp >= start_date,
        ActivityLog.timestamp < end_date
    ).limit(5).to_list()
    for log in logs4:
        print(f"[{log.timestamp}] User {log.user_id}: {log.action_type}")

    print(f"\n--- 5. Hae {user1.username}:n viimeisimmät 5 project-lokia (Sort, limit, filter) ---")
    print(f"\n--- Haku 6: Hae {user1.username}:n viimeisimmät 5 project-lokia (Sort, limit, filter) ---")
    logs5 = await ActivityLog.find(
        ActivityLog.user_id == user1.id,
        ActivityLog.action_type == "project_created"
    ).sort("-timestamp").limit(5).to_list()
    for log in logs5:
        print(f"[{log.timestamp}] User {log.user_id}: {log.action_type}")

    print("\n--- 6. Monimutkainen yhdistelmähaku ---")
    print("\n--- Haku 7: Monimutkainen yhdistelmähaku ---")
    one_week_ago = now - timedelta(days=7)
    logs6 = await ActivityLog.find(
        Or(
            ActivityLog.user_id == user1.id,
            ActivityLog.user_id == user2.id
        ),
        Or(
            ActivityLog.action_type == "project_created",
            ActivityLog.action_type == "task_created"
        ),
        ActivityLog.timestamp >= one_week_ago
    ).sort("-timestamp").limit(10).to_list()
    for log in logs6:
        print(f"[{log.timestamp}] User {log.user_id}: {log.action_type}")

if __name__ == "__main__":
    asyncio.run(main())