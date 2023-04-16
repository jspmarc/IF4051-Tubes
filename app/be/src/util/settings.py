from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    api_token: str | None = None
    """
    API Token already hashed
    """

    mqtt_host: str = "127.0.0.1"
    mqtt_port: int = 1883
    mqtt_user: str | None = None
    mqtt_pass: str | None = None

    app_state_sqlite_url: str = "sqlite:///./app_state.db"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
