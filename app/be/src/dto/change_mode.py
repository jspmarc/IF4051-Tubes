from pydantic import BaseModel

from util.enums import AppMode


class ChangeMode(BaseModel):
    current_mode: AppMode
