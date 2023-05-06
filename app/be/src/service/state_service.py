import asyncio
from typing import Annotated
from fastapi import Depends
from redis import Redis
from functools import partial

import dto
from util import Constants
from service.websocket_service import WebsocketService
from service import MqttService
from util.database import get_state_db


class StateService:
    _lock = asyncio.Lock()

    def __init__(
        self,
        db: Annotated[Redis, Depends(get_state_db)],
        websocket_service: Annotated[WebsocketService, Depends()],
        mqtt_service: Annotated[MqttService, Depends(MqttService.get_instance)],
    ):
        self.__db = db
        self.__ws = websocket_service
        self.__mqtt = mqtt_service

    def get_state(self) -> dto.AppState:
        state = self.__db.get(Constants.REDIS_STATE_KEY)
        if state is None:
            raise RuntimeError("No state found in database")
        return dto.AppState.parse_raw(state)

    async def __save_to_db(self, new_state: dto.AppState) -> dto.AppState:
        db = self.__db

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, partial(db.set, Constants.REDIS_STATE_KEY, new_state.json())
        )

        return new_state

    async def update_state(self, new_state: dto.AppState) -> dto.AppState:
        task_broadcast = asyncio.create_task(self.__ws.broadcast_state(new_state))
        task_save = asyncio.create_task(self.__save_to_db(new_state))

        async with self._lock:
            current_state = self.get_state()
            if current_state.servo_multiple != new_state.servo_multiple:
                # IMO, agak janky, tapi "yasudalaya"
                self.__mqtt.publish_servo(new_state.servo_multiple)
            (_, db_state) = await asyncio.gather(task_broadcast, task_save)
            return db_state
