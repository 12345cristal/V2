from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List

from app.core.security import decode_token_ws  # función que valida JWT en query
from app.api.deps import get_db

router = APIRouter()

active_connections: Dict[int, List[WebSocket]] = {}


async def connect_user(user_id: int, websocket: WebSocket):
    await websocket.accept()
    if user_id not in active_connections:
        active_connections[user_id] = []
    active_connections[user_id].append(websocket)


async def disconnect_user(user_id: int, websocket: WebSocket):
    if user_id in active_connections:
        active_connections[user_id].remove(websocket)
        if not active_connections[user_id]:
            active_connections.pop(user_id)


async def send_to_user(user_id: int, message: dict):
    if user_id in active_connections:
        for ws in active_connections[user_id]:
            await ws.send_json(message)


@router.websocket("/ws/notificaciones")
async def websocket_notificaciones(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    user = decode_token_ws(token)  # debe devolver user_id, rol, etc.
    user_id = user["id"]

    await connect_user(user_id, websocket)
    try:
        while True:
            # si quieres recibir mensajes del cliente
            await websocket.receive_text()
    except WebSocketDisconnect:
        await disconnect_user(user_id, websocket)
