from pydantic import BaseModel, Field


class RotateServo(BaseModel):
    multiple: int = Field(
        description="Multiple of 45º, for example when multiple is 2, servo rotation is 90º.\
                     Value range: [0,2].",
        ge=0,
        le=2,
    )
