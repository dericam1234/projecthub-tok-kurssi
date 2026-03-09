"""
migrations/env.py
─────────────────
Alembic environment configuration.

This file tells Alembic:
  1. Where to find the database URL  → from app.config.settings
  2. Which metadata to diff against  → SQLModel.metadata (all table=True models)

Usage:
  alembic revision --autogenerate -m "initial tables"   # generate migration
  alembic upgrade head                                   # apply migrations
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

from app.config import settings

# ── Import all SQL models so their tables are registered on the metadata ──
from app.models.sql_models import (
    User,
    Project,
    ProjectUserLink,
    Task,
    TaskTagLink,
    Tag,
)  # noqa: F401

# Alembic Config object — provides access to alembic.ini values.
config = context.config

# Override the URL from alembic.ini with the value from our settings.
config.set_main_option("sqlalchemy.url", settings.postgres_url)

# Set up Python logging from alembic.ini [loggers] section.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The target metadata Alembic will diff against when auto-generating
# migrations.  SQLModel.metadata contains every table=True model.
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    In this mode Alembic generates SQL scripts without connecting to
    the database — useful for reviewing changes before applying them.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Alembic connects to the database and applies changes directly.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
