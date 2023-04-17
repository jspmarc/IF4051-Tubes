from sqlalchemy import BigInteger, Column, Double
from common_python.model.base import CommonBase


class Mq135(CommonBase):
    __tablename__ = "mq135"

    co2 = Column(Double)
    created_timestamp = Column(BigInteger, primary_key=True, index=True)
