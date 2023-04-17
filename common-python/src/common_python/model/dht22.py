from sqlalchemy import BigInteger, Column, Double
from common_python.model.base import CommonBase


class Dht22(CommonBase):
    __tablename__ = "dht22"

    humidity = Column(Double)
    temperature = Column(Double)
    created_timestamp = Column(BigInteger, primary_key=True, index=True)
