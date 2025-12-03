# app/api/v1/sockets/notifications_ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws", tags=["notifications-ws"])

# podrías relacionar usuario_id con el socket para mandar notifs dirigidas
connections: dict[int, WebSocket] = {}


@router.websocket("/notificaciones/{usuario_id}")
async def websocket_notifications(websocket: WebSocket, usuario_id: int):
    await websocket.accept()
    connections[usuario_id] = websocket
    try:
        while True:
            await websocket.receive_text()  # opcional: ping client
    except WebSocketDisconnect:
        if usuario_id in connections:
            del connections[usuario_id]
