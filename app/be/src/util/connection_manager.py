from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    def __len__(self) -> int:
        return len(self.active_connections)

    async def connect(self, websocket: WebSocket) -> None:
        """
        Connect client
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """
        Disconnect client
        """
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        """
        Send message to specific client
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        """
        Send message to all connected clients
        """
        for connection in self.active_connections:
            await connection.send_text(message)
