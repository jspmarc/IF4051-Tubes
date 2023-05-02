from pydantic import BaseModel
from datetime import datetime

from util.enums import AlertType


class Alert(BaseModel):
    alert_type: AlertType
    alert_description: str
    alert_time: str | datetime
