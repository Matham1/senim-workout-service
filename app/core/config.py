from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Basira Workout Tracker"
    REDIS_URL: str = "redis://redis:6379/0"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/senim"
    class Config:
        env_file = ".env"

settings = Settings()
print(f"Database URL: {settings.DATABASE_URL}")  # Debug: print DB URL at startup