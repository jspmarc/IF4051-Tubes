import dto

from typing import Annotated
from fastapi import Depends, status

from service import MqttService, StateService


class ServoService:
    def __init__(
        self,
        mqtt_service: Annotated[MqttService, Depends(MqttService.get_instance)],
        state_service: Annotated[StateService, Depends()],
    ):
        self.__mqtt_service = mqtt_service
        self.__state_service = state_service

    async def update_rotation(self, servo_multiple: int, save_to_db: bool = True):
        if servo_multiple < 0 or servo_multiple > 2:
            raise ValueError("servo_scale has to be [0..2]")
        self.__mqtt_service.publish_servo(servo_multiple)

        state = self.__state_service.get_state()
        # create new if state is None
        if state is None:
            state = dto.AppState()
        state.servo_multiple = servo_multiple
        if save_to_db:
            return await self.__state_service.update_state(state)
        return state

    def get_rotation_multiple(self):
        state = self.__state_service.get_state()
        if state is None:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        return state.servo_multiple
