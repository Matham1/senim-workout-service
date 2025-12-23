from pydantic_settings import BaseSettings
from os import getenv
class Settings(BaseSettings):
    PROJECT_NAME: str = "Basira Workout Tracker"
    REDIS_URL: str = getenv("REDIS_URL", "redis://redis:6379/0")
    DATABASE_URL: str = getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/senim")
    class Config:
        env_file = ".env"

settings = Settings()