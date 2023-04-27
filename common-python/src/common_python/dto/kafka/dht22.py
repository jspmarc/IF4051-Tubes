from pydantic import BaseModel


class KafkaDht22(BaseModel):
    humidity_avg: float = 0
    humidity_min: float = 0
    humidity_max: float = 0
    temperature_avg: float = 0
    temperature_min: float = 0
    temperature_max: float = 0
    created_timestamp: int = 0
