from pydantic import BaseModel


class KafkaDht22(BaseModel):
    humidity_avg: float
    humidity_min: float
    humidity_max: float
    temperature_avg: float
    temperature_min: float
    temperature_max: float
    created_timestamp: int
