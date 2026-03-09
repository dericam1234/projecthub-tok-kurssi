"""
app/config.py
─────────────
Centralised configuration using pydantic-settings.

Values are loaded from environment variables or an `.env` file located in the
project root.  Copy `.env.example` to `.env` before running the application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide settings read from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",       # automatically load .env when present
        env_file_encoding="utf-8",
        extra="ignore",        # ignore unknown env vars
    )

    # ── PostgreSQL ──────────────────────────────────────────────────
    postgres_url: str = (
        "postgresql://projecthub:projecthub_secret@localhost:5432/projecthub_db"
    )

    # ── MongoDB ─────────────────────────────────────────────────────
    mongo_url: str = "mongodb://projecthub:projecthub_secret@localhost:27017"
    mongo_db_name: str = "projecthub_logs"

    # ── Redis ───────────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"


# Singleton instance — import this wherever settings are needed.
settings = Settings()
