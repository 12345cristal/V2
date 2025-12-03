# app/services/chat_service.py
from typing import Dict, List
from fastapi import WebSocket


class ChatManager:
    """
    Maneja conexiones WebSocket para chat sencillo por sala.
    """

    def __init__(self) -> None:
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.setdefault(room, []).append(websocket)

    def disconnect(self, room: str, websocket: WebSocket) -> None:
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)
            if not self.active_connections[room]:
                del self.active_connections[room]

    async def broadcast(self, room: str, message: str) -> None:
        for ws in self.active_connections.get(room, []):
            await ws.send_text(message)


chat_manager = ChatManager()
