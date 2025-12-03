# app/api/v1/sockets/notifications_ws.py
from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["ws-notificaciones"])

connections: Dict[int, WebSocket] = {}


@router.websocket("/ws/notificaciones/{usuario_id}")
async def websocket_notifications(websocket: WebSocket, usuario_id: int):
    await websocket.accept()
    connections[usuario_id] = websocket
    try:
        while True:
            # podrías manejar mensajes entrantes si quieres
            await websocket.receive_text()
    except WebSocketDisconnect:
        if usuario_id in connections:
            del connections[usuario_id]
