from pydantic import BaseModel


class KafkaMq135(BaseModel):
    co2_avg: float
    co2_min: float
    co2_max: float
    created_timestamp: int
