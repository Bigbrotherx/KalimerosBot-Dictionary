from functools import lru_cache

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


def get_db_url():
    settings = get_settings()
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
