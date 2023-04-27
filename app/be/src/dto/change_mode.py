from pydantic import BaseModel, Field, validator

from util.enums import AppMode


class ChangeMode(BaseModel):
    current_mode: AppMode
