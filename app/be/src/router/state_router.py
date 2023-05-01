from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    status
)

from dto import AppState
from service import StateService, WebsocketService


state_router = APIRouter(prefix="/state", tags=["State"])


@state_router.get("", response_model=AppState)
def get_state(state_service: Annotated[StateService, Depends()]):
    state = state_service.get_state()
    if state is None:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return state


@state_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    state_service: Annotated[StateService, Depends()],
    websocket_service: Annotated[WebsocketService, Depends()],
):
    await websocket_service.connect(websocket)
    # send current state to the new connected client
    curr_state = state_service.get_state()
    await websocket_service.send_state(curr_state, websocket)
    try:
        while True:
            # get new state from client
            data = await websocket.receive_json()
            new_state_req: AppState = AppState.from_dict(data)
            # update state in database
            await state_service.update_state(new_state_req)
    except WebSocketDisconnect:
        websocket_service.disconnect(websocket)
