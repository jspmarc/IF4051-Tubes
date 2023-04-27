from typing import List
from pydantic import BaseModel

from common_python.dto import KafkaDht22, KafkaMq135
from .alarm import Alarm
from util.enums import AppMode


class AppState(BaseModel):
    current_mode: AppMode = AppMode.Override
    servo_multiple: int = 0
    active_alarms: List[Alarm] = []
    dht22_statistics = KafkaDht22()
    mq135_statistics = KafkaMq135()

    class Config:
        orm_mode = True
        use_enum_values = True
