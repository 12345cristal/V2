# app/services/chat_service.py
from typing import Dict, List
from fastapi import WebSocket


class ChatManager:
    """
    Maneja conexiones WebSocket por sala de chat.
    """

    def __init__(self) -> None:
        self.rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.rooms.setdefault(room, []).append(websocket)

    def disconnect(self, room: str, websocket: WebSocket) -> None:
        if room in self.rooms and websocket in self.rooms[room]:
            self.rooms[room].remove(websocket)
            if not self.rooms[room]:
                del self.rooms[room]

    async def broadcast(self, room: str, message: str) -> None:
        for ws in self.rooms.get(room, []):
            await ws.send_text(message)


chat_manager = ChatManager()
