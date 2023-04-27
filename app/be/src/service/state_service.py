from typing import Annotated
from fastapi import Depends
from redis import Redis

import dto
from util import Constants
from util.database import get_state_db


class StateService:
    def __init__(self, db: Annotated[Redis, Depends(get_state_db)]):
        self.__db = db

    def get_state(self) -> dto.AppState:
        state = self.__db.get(Constants.REDIS_STATE_KEY)
        if state is None:
            raise RuntimeError("No state found in database")
        return dto.AppState.parse_raw(state)

    def update_state(self, new_state: dto.AppState) -> dto.AppState:
        db = self.__db

        db.set(Constants.REDIS_STATE_KEY, new_state.json())

        return new_state
