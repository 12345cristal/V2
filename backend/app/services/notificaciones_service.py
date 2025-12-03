# app/services/notificaciones_service.py
from typing import Optional
from fastapi import WebSocket

from app.api.v1.sockets.notifications_ws import connections


async def push_notification(usuario_id: int, payload: str) -> None:
    ws: Optional[WebSocket] = connections.get(usuario_id)
    if ws:
        await ws.send_text(payload)
