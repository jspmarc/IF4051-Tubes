from pydantic import BaseModel


class KafkaMq135(BaseModel):
    co2_avg: float = 0
    co2_min: float = 0
    co2_max: float = 0
    created_timestamp: int = 0
