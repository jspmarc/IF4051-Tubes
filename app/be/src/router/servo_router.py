from typing import Annotated
from fastapi import APIRouter, Depends, Body, status

from dto import RotateServoRequest
from service import ServoService


servo_router = APIRouter(
    prefix="/servo",
)


@servo_router.post(
    "",
    status_code=status.HTTP_204_NO_CONTENT
)
def rotate_servo(
    request: Annotated[RotateServoRequest, Body()],
    servo_service: Annotated[ServoService, Depends(use_cache=True)],
):
    servo_service.update_rotation(request.multiple)
    return request


@servo_router.get(
    "",
    response_model=RotateServoRequest
)
def get_servo_multiple(
    servo_service: Annotated[ServoService, Depends()],
):
    return {"multiple": servo_service.get_rotation_multiple()}
