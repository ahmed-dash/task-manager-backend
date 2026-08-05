"""
Centralized application configuration.

All values are read from environment variables (or a local .env file when
running outside Docker). Nothing sensitive is hard-coded here — in
production these are injected as real environment variables / Docker
secrets / Jenkins credentials, never committed to git.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- General ---
    PROJECT_NAME: str = "Task Manager API"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"  # development | staging | production

    # --- Security / JWT ---
    SECRET_KEY: str = "change-me-in-env"  # override via env var in every real deployment
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # --- Database ---
    DATABASE_URL: str = "postgresql+psycopg2://taskuser:taskpass@db:5432/taskmanager"

    # --- CORS ---
    # Comma-separated list of allowed origins, e.g. "http://localhost:5173,https://myapp.com"
    CORS_ORIGINS: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
