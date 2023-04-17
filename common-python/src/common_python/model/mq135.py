from sqlalchemy import TIMESTAMP, Column, Double
from common_python.model.base import CommonBase


class Mq135(CommonBase):
    __tablename__ = "Mq135"

    co2 = Column(Double)
    created_timestamp = Column(TIMESTAMP, primary_key=True, index=True)
