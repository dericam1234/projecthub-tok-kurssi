# ProjectHub — Backend Data Layer

A template for the project in the "Tietokannan ohjelmallinen käyttö" -course.

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Docker and Docker Compose

## How to run

1. **Create the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the infrastructure:**

   ```bash
   docker compose up -d
   ```

   This launches PostgreSQL, MongoDB, and Redis in the background with persistent volumes.

3. **Install dependencies:**

   ```bash
   uv sync
   ```

   This creates a virtual environment in `.venv` and installs all packages declared in `pyproject.toml`. A `uv.lock` lockfile is generated automatically to pin exact versions.

4. **Run the script:**

   ```bash
   uv run python -m app.main
   ```

   This is the "playground" where we can test how services function.

   > Since this isn't an actual app that would do something, we need to play pretend.

5. **Working with Alembic migrations** (optional):

   ```bash
   # Generate a migration from the current models
   uv run alembic revision --autogenerate -m "initial tables"

   # Apply all pending migrations
   uv run alembic upgrade head
   ```

## Adding or updating dependencies

```bash
uv add <package>           # add a new dependency
uv remove <package>        # remove a dependency
uv lock --upgrade          # upgrade all packages to latest compatible versions
```

## Stopping the infrastructure

```bash
docker compose down       # stop containers, keep data
docker compose down -v    # stop containers and delete all data
```

## Project structure

```
.
├── pyproject.toml              # Project metadata and dependencies
├── uv.lock                     # Lockfile (auto-generated, commit to VCS)
├── docker-compose.yml          # Postgres 16, Mongo 7, Redis 7
├── .env.example                # Connection string template
├── alembic.ini                 # Alembic configuration
│
├── app/
│   ├── config.py               # pydantic-settings (single source of truth)
│   ├── database/
│   │   ├── sql_db.py           # SQLModel engine + session helper
│   │   ├── mongo_db.py         # PyMongo async client + Beanie init
│   │   └── redis_client.py     # Redis client
│   ├── models/
│   │   ├── sql_models.py       # User, Project, Task (PostgreSQL)
│   │   └── mongo_models.py     # ActivityLog (MongoDB)
│   ├── services/
│   │   ├── project_service.py  # SQL CRUD operations
│   │   ├── log_service.py      # MongoDB CRUD operations
│   │   └── cache_service.py    # Redis caching logic
│   └── main.py                 # Entry point
│
└── migrations/
    ├── env.py                  # Alembic environment
    └── script.py.mako          # Migration file template
```
