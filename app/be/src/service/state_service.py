import asyncio
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

import dto
import models
from service.websocket_service import WebsocketService
from util.database import get_state_db


class StateService:
    def __init__(
        self,
        db: Annotated[Session, Depends(get_state_db)],
        websocket_service: Annotated[WebsocketService, Depends()],
    ):
        self.__db = db
        self.__ws = websocket_service

    def get_state(self) -> dto.AppState:
        state = dto.AppState.from_orm(self.__db.query(models.AppState).one_or_none())
        if state is None:
            raise RuntimeError("No state found in database")
        return state

    async def __save_to_db(self, new_state: dto.AppState) -> dto.AppState:
        db = self.__db
        query = db.query(models.AppState)
        db_state = query.one_or_none()
        # create new if state is None
        if db_state is None:
            db_state = models.AppState()

        for var, value in vars(new_state).items():
            setattr(db_state, var, value)

        db.add(db_state)
        db.commit()
        db.refresh(db_state)

        return db_state

    async def update_state(self, new_state: dto.AppState) -> dto.AppState:
        task_broadcast = asyncio.create_task(self.__ws.broadcast_state(new_state))
        task_save = asyncio.create_task(self.__save_to_db(new_state))

        (_, db_state) = await asyncio.gather(task_broadcast, task_save)

        return dto.AppState.from_orm(db_state)
