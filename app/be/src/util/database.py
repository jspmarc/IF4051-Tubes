from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import json
from pydantic.json import pydantic_encoder

from util.settings import get_settings


def __custom_json_serializer(*args, **kwargs) -> str:
    """
    Encodes json in the same way that pydantic does.
    source: https://stackoverflow.com/a/68714342
    """
    return json.dumps(*args, default=pydantic_encoder, **kwargs)


def get_state_db():
    db = AppStateSession()
    try:
        yield db
    finally:
        db.close()


BaseSqlModel = declarative_base()

app_state_engine = create_engine(
    get_settings().app_state_sqlite_url,
    connect_args={"check_same_thread": False},
    json_serializer=__custom_json_serializer,
)
AppStateSession = sessionmaker(autocommit=False, autoflush=False, bind=app_state_engine)
