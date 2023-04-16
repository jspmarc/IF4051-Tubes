from typing import Annotated
from fastapi import APIRouter, Depends, Body, status

from dto import RotateServo
from service import ServoService


servo_router = APIRouter(prefix="/servo", tags=["Servo"])


@servo_router.post("", status_code=status.HTTP_204_NO_CONTENT)
def rotate_servo(
    request: Annotated[RotateServo, Body()],
    servo_service: Annotated[ServoService, Depends()],
):
    servo_service.update_rotation(request.multiple)


@servo_router.post("/open", status_code=status.HTTP_204_NO_CONTENT)
def open_servo(
    servo_service: Annotated[ServoService, Depends()],
):
    servo_service.update_rotation(2)


@servo_router.post("/close", status_code=status.HTTP_204_NO_CONTENT)
def close_servo(
    servo_service: Annotated[ServoService, Depends()],
):
    servo_service.update_rotation(0)


@servo_router.get("", response_model=RotateServo)
def get_servo_multiple(
    servo_service: Annotated[ServoService, Depends()],
):
    return {"multiple": servo_service.get_rotation_multiple()}