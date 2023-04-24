from pydantic import BaseModel, Field, validator

from util.enums import AppMode


class ChangeMode(BaseModel):
    current_mode: str = Field(
        description="Ai or Override",
    )

    @validator('current_mode')
    def mode_validator(cls, mode):
        if mode not in AppMode:
            raise ValueError('Mode must be Ai or Override')
        return mode
