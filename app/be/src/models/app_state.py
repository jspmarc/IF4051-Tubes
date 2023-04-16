from sqlalchemy import Column, Integer, Enum, JSON

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
