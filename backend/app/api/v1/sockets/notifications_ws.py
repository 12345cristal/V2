# app/api/v1/sockets/notifications_ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["ws-notificaciones"])

_connections: dict[int, WebSocket] = {}


@router.websocket("/ws/notificaciones/{usuario_id}")
async def websocket_notifications(websocket: WebSocket, usuario_id: int):
    await websocket.accept()
    _connections[usuario_id] = websocket
    try:
        while True:
            await websocket.receive_text()  # podrías manejar pings si quieres
    except WebSocketDisconnect:
        if usuario_id in _connections:
            del _connections[usuario_id]


async def push_notification_ws(usuario_id: int, payload: str) -> None:
    ws = _connections.get(usuario_id)
    if ws:
        await ws.send_text(payload)
