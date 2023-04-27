from typing import Annotated
from fastapi import (
    APIRouter, 
    Depends, 
    WebSocket, 
    WebSocketDisconnect, 
    status
)
from util.connection_manager import ConnectionManager

from dto import AppState
from service.state_service import StateService


state_router = APIRouter(prefix="/state", tags=["State"])
connection_manager = ConnectionManager()

@state_router.get("", response_model=AppState)
def get_state(state_service: Annotated[StateService, Depends()]):
    state = state_service.get_state()
    if state is None:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return state


@state_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
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
            new_state_req: AppState = AppState.from_dict(data)
            # update state in database
            new_state = state_service.update_state(new_state_req)
            # broadcast new state to all clients
            await connection_manager.broadcast_state(new_state)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
