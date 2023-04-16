from typing import Annotated

from fastapi import Depends

from service import MqttService


class ServoService:
    def __init__(
        self, mqtt_service: Annotated[MqttService, Depends(MqttService.get_instance)]
    ):
        self.__mqtt_service = mqtt_service
        self.__rotation_multiple = 0

    def update_rotation(self, servo_multiple: int):
        if servo_multiple < 0 or servo_multiple > 2:
            raise ValueError("servo_scale has to be [0..2]")
        self.__mqtt_service.publish_servo(servo_multiple)
        self.__rotation_multiple = servo_multiple

    def get_rotation_multiple(self):
        return self.__rotation_multiple
