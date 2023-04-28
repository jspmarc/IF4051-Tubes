from typing import Annotated
from fastapi import APIRouter, Depends, Body, WebSocket, WebSocketDisconnect, status
from util.connection_manager import ConnectionManager
from service.state_service import StateService

from dto import RotateServo
from service import ServoService


servo_router = APIRouter(prefix="/servo", tags=["Servo"])
connection_manager = ConnectionManager()

@servo_router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def rotate_servo(
    request: Annotated[RotateServo, Body()],
    servo_service: Annotated[ServoService, Depends()],
):
    new_state = servo_service.update_rotation(request.servo_multiple)
    await connection_manager.broadcast_state(new_state)


@servo_router.post("/open", status_code=status.HTTP_204_NO_CONTENT)
async def open_servo(
    servo_service: Annotated[ServoService, Depends()],
):
    new_state = servo_service.update_rotation(2)
    await connection_manager.broadcast_state(new_state)


@servo_router.post("/close", status_code=status.HTTP_204_NO_CONTENT)
async def close_servo(
    servo_service: Annotated[ServoService, Depends()],
):
    new_state = servo_service.update_rotation(0)
    await connection_manager.broadcast_state(new_state)


@servo_router.get("", response_model=RotateServo)
def get_servo_multiple(
    servo_service: Annotated[ServoService, Depends()],
):
    return {"servo_multiple": servo_service.get_rotation_multiple()}
