from functools import lru_cache
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
