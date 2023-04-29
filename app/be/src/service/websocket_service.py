from typing import List
from fastapi import WebSocket

import dto


class WebsocketService:
    _active_connections: List[WebSocket] = []

    def __len__(self) -> int:
        return len(self._active_connections)

    async def connect(self, websocket: WebSocket) -> None:
        """
        Connect client
        """
        await websocket.accept()
        self._active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """
        Disconnect client
        """
        self._active_connections.remove(websocket)

    async def send_state(self, state: dto.AppState, websocket: WebSocket) -> None:
        """
        Send `AppState` to specific client
        """
        await websocket.send_text(state.json())

    async def broadcast_state(self, state: dto.AppState) -> None:
        """
        Send `AppState` to all connected clients
        """
        state_json = state.json()
        for connection in self._active_connections:
            await connection.send_text(state_json)
