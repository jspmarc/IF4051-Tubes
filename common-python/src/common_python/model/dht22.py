from sqlalchemy import TIMESTAMP, Column, Double
from common_python.model.base import CommonBase


class Dht22(CommonBase):
    __tablename__ = "Dht22"

    humidity = Column(Double)
    temperature = Column(Double)
    created_timestamp = Column(TIMESTAMP, primary_key=True, index=True)
