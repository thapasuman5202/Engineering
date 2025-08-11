from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "God Mode Ultra Flow"
    database_url: str = "sqlite:///./app.db"
    secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    cors_origins: list[str] = ["*"]
    redis_url: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
