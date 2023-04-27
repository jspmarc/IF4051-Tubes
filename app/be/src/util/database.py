from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import json
from pydantic.json import pydantic_encoder
from redis import Redis

from dto.app_state import AppState
from util import Constants
from util.settings import get_settings

__settings = get_settings()

if __settings.redis_password != "":
    __redis = Redis(
        host=__settings.redis_host,
        port=__settings.redis_port,
        password=__settings.redis_password,
        decode_responses=True,
    )
else:
    __redis = Redis(
        host=__settings.redis_host,
        port=__settings.redis_port,
        decode_responses=True,
    )


def __custom_json_serializer(*args, **kwargs) -> str:
    """
    Encodes json in the same way that pydantic does.
    source: https://stackoverflow.com/a/68714342
    """
    return json.dumps(*args, default=pydantic_encoder, **kwargs)


def initialize_db():
    state = __redis.get(Constants.REDIS_STATE_KEY)
    if state is None:
        state = AppState()
        __redis.set(Constants.REDIS_STATE_KEY, state.json())
        return

    try:
        AppState.parse_raw(state)
    except Exception:
        state = AppState()
        __redis.set(Constants.REDIS_STATE_KEY, state.json())
        return


@lru_cache()
def get_state_db():
    return __redis


BaseSqlModel = declarative_base()

__app_state_engine = create_engine(
    __settings.app_state_sqlite_url,
    connect_args={"check_same_thread": False},
    json_serializer=__custom_json_serializer,
)
AppStateSession = sessionmaker(autocommit=False, autoflush=False, bind=__app_state_engine)
