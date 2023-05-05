from __future__ import annotations
from typing import Annotated
from fastapi import Depends
import paho.mqtt.client as mqtt

from util.settings import Settings, get_settings
from util import Constants


class MqttService:
    __instance: MqttService | None = None

    def __init__(self, settings: Settings):
        """
        Treat this constructor/init as private. Never directly invoke this constructor.
        """
        if self.__instance:
            return

        mqtt_port = settings.mqtt_port
        mqtt_host = settings.mqtt_host
        mqtt_user = settings.mqtt_user
        mqtt_pass = settings.mqtt_pass

        self.__client = mqtt.Client()
        if mqtt_user is not None and mqtt_pass is not None:
            self.__client.username_pw_set(mqtt_user, mqtt_pass)
        self.__client.connect(mqtt_host, mqtt_port)

    def publish_servo(self, multiple: int):
        topic = Constants.MQTT_SERVO_TOPIC
        self.__client.publish(topic, multiple, qos=1, retain=True)

    def disconnect(self):
        self.__client.disconnect()

    @classmethod
    def get_instance(cls, settings: Annotated[Settings, Depends(get_settings)]):
        instance = cls.__instance

        if instance is None:
            instance = MqttService(settings)
            cls.__instance = instance

        return instance
