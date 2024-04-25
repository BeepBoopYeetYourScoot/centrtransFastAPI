import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class TestSettings(Settings): ...


class LocalSettings(Settings): ...


class ProductionSettings(Settings):
    DEBUG: bool = False


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "test": TestSettings(),
        "local": LocalSettings(),
        "prod": ProductionSettings(),
    }
    return config_type[env]


settings: Settings = get_config()
