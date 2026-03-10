import asyncio

import asyncio

from app.database.sql_db import create_db_and_tables, get_session
from app.models.sql_models import Check


async def main() -> None:
    create_db_and_tables()

    new_check = Check(description="Testataan tietokantayhteys", status="OK")

    with get_session() as session:
        session.add(new_check)
        session.commit()
        session.refresh(new_check)

        print(f"uusi check luotu id:llä {new_check.id}")



if __name__ == "__main__":
    asyncio.run(main())
