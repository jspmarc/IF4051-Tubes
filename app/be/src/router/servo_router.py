from typing import Annotated
from fastapi import APIRouter, Depends, Body, WebSocket, WebSocketDisconnect, status
from util.connection_manager import ConnectionManager
from service.state_service import StateService

from dto import RotateServo
from service import ServoService


servo_router = APIRouter(prefix="/servo", tags=["Servo"])
connection_manager = ConnectionManager()

@servo_router.post("", status_code=status.HTTP_204_NO_CONTENT)
def rotate_servo(
    request: Annotated[RotateServo, Body()],
    servo_service: Annotated[ServoService, Depends()],
):
    servo_service.update_rotation(request.servo_multiple)


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
    return {"servo_multiple": servo_service.get_rotation_multiple()}

@servo_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    servo_service: Annotated[ServoService, Depends()],
    state_service: Annotated[StateService, Depends()]
):
    await connection_manager.connect(websocket)
    # send current state to the new connected client
    curr_state = state_service.get_state()
    await connection_manager.send_state(curr_state, websocket)
    try:
        while True:
            # get new state from client
            data = await websocket.receive_json()
            new_state_req: RotateServo = RotateServo.from_dict(data)
            # update state in database
            new_state = servo_service.update_rotation(new_state_req.servo_multiple)
            # broadcast new state to all clients
            await connection_manager.broadcast_state(new_state)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
