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

    db_uri: str = "http://localhost:8086"
    db_token: str = ""
    db_org: str = ""
    db_bucket: str = ""

    kafka_bootstrap_server: str = "127.0.0.1:9092"

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_password: str = ""

    gmail_sender_email: str = ""
    gmail_password: str = ""
    notification_receiver_email: str = ""

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
