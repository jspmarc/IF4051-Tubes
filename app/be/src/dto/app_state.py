from typing import List
from pydantic import BaseModel

from .alarm import Alarm
from util.enums import AppMode


class AppState(BaseModel):
    current_mode: AppMode
    servo_multiple: int
    active_alarms: List[Alarm]

    class Config:
        orm_mode = True
        use_enum_values = True
