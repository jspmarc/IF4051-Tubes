from typing import Annotated

from fastapi import APIRouter, Depends, Body

from dto.request import RotateServoRequest
from service import ServoService


servo_router = APIRouter(
    prefix="/servo",
)


@servo_router.post("", status_code=204)
def rotate_servo(
    request: Annotated[RotateServoRequest, Body()],
    servo_service: Annotated[ServoService, Depends(use_cache=True)],
):
    print(servo_service)
    servo_service.update_rotation(request.multiple)


@servo_router.get("", status_code=200)
def get_servo_scale(
    servo_service: Annotated[ServoService, Depends()],
):
    print(servo_service)
    return {"rotation": servo_service.get_rotation_scale()}
