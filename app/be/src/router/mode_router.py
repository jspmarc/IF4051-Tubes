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
async def change_mode(
    request: Annotated[ChangeMode, Body()],
    mode_service: Annotated[ModeService, Depends()],
):
    new_state = mode_service.update_mode(request.current_mode)
    await connection_manager.broadcast_state(new_state)


@mode_router.post("/ai", status_code=status.HTTP_204_NO_CONTENT)
async def ai_mode(
    mode_service: Annotated[ModeService, Depends()],
):
    new_state = mode_service.update_mode(AppMode.Ai)
    await connection_manager.broadcast_state(new_state)


@mode_router.post("/override", status_code=status.HTTP_204_NO_CONTENT)
async def override_mode(
    mode_service: Annotated[ModeService, Depends()],
):
    new_state = mode_service.update_mode(AppMode.Override)
    await connection_manager.broadcast_state(new_state)


@mode_router.get("", response_model=ChangeMode)
def get_mode(
    mode_service: Annotated[ModeService, Depends()],
):
    return {"current_mode": mode_service.get_mode()}
