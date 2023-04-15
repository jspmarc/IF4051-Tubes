from typing import Annotated

from fastapi import Depends

from service import MqttService


class ServoService:
    def __init__(self, mqtt_service: Annotated[MqttService, Depends()]):
        self.__mqtt_service = mqtt_service
        self.__rotation_scale = 0

    def update_rotation(self, servo_scale: int):
        if servo_scale < 0 or servo_scale > 2:
            raise ValueError("servo_scale has to be [0..2]")
        self.__rotation_scale = servo_scale

    def get_rotation_scale(self):
        return self.__rotation_scale
