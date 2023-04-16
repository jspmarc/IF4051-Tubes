from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    mqtt_host: str = "127.0.0.1"
    mqtt_port: int = 1883
    mqtt_user: str | None = None
    mqtt_pass: str | None = None

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
