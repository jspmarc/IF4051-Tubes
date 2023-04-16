from typing import Annotated
from fastapi import Depends

from service import MqttService, StateService


class ServoService:
    def __init__(
        self,
        mqtt_service: Annotated[MqttService, Depends(MqttService.get_instance)],
        state_service: Annotated[StateService, Depends()],
    ):
        self.__mqtt_service = mqtt_service
        self.__state_service = state_service

    def update_rotation(self, servo_multiple: int):
        if servo_multiple < 0 or servo_multiple > 2:
            raise ValueError("servo_scale has to be [0..2]")
        self.__mqtt_service.publish_servo(servo_multiple)

        state = self.__state_service.get_state()
        state.servo_multiple = servo_multiple
        return self.__state_service.update_state(state)

    def get_rotation_multiple(self):
        return self.__state_service.get_state().servo_multiple
