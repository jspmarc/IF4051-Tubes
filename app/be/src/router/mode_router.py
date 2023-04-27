from typing import Annotated
from fastapi import APIRouter, Depends, Body, WebSocket, WebSocketDisconnect, status
from service.state_service import StateService
from util.connection_manager import ConnectionManager
from util.enums import AppMode

from dto import ChangeMode
from service import ModeService


mode_router = APIRouter(prefix="/mode", tags=["Mode"])
connection_manager = ConnectionManager()

@mode_router.post("", status_code=status.HTTP_204_NO_CONTENT)
def change_mode(
    request: Annotated[ChangeMode, Body()],
    mode_service: Annotated[ModeService, Depends()],
):
    mode_service.update_mode(request.current_mode)


@mode_router.post("/ai", status_code=status.HTTP_204_NO_CONTENT)
def ai_mode(
    mode_service: Annotated[ModeService, Depends()],
):
    mode_service.update_mode(AppMode.Ai)


@mode_router.post("/override", status_code=status.HTTP_204_NO_CONTENT)
def override_mode(
    mode_service: Annotated[ModeService, Depends()],
):
    mode_service.update_mode(AppMode.Override)


@mode_router.get("", response_model=ChangeMode)
def get_mode(
    mode_service: Annotated[ModeService, Depends()],
):
    return {"current_mode": mode_service.get_mode()}

@mode_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    mode_service: Annotated[ModeService, Depends()],
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
            new_state_req: ChangeMode = ChangeMode.from_dict(data)
            # update state in database
            new_state = mode_service.update_mode(new_state_req.current_mode)
            # broadcast new state to all clients
            await connection_manager.broadcast_state(new_state)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
