from sqlalchemy import JSON, Column, Integer, Enum

from common_python.dto import KafkaMq135, KafkaDht22
from common_python.model import PydanticJson
# from dto.alarm import Alarm
from util.enums import AppMode
from util.database import BaseSqlModel


class AppState(BaseSqlModel):
    __tablename__ = "state"

    id = Column(Integer, primary_key=True, index=False)
    current_mode = Column(Enum(AppMode))
    servo_multiple = Column(Integer)
    active_alarms = Column(JSON)
    """
    List of dto.Alarms
    """
    dht22_statistics = Column(PydanticJson(KafkaDht22))
    mq135_statistics = Column(PydanticJson(KafkaMq135))
