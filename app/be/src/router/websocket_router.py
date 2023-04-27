from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from util.connection_manager import ConnectionManager

ws_router = APIRouter(prefix="/ws", tags=["WebSocket"])
connection_manager = ConnectionManager()

@ws_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_personal_message(f"You wrote: {data}", websocket)
            await connection_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(f"Client #{client_id} left the chat")