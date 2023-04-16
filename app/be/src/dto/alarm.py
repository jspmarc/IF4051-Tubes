from pydantic import BaseModel


class Alarm(BaseModel):
    tmp: str
