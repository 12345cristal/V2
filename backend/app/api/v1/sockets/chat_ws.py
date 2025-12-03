# app/api/v1/sockets/chat_ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.chat_service import chat_manager

router = APIRouter(prefix="/ws", tags=["chat-ws"])


@router.websocket("/chat/{room}")
async def websocket_chat(websocket: WebSocket, room: str):
    await chat_manager.connect(room, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await chat_manager.broadcast(room, data)
    except WebSocketDisconnect:
        chat_manager.disconnect(room, websocket)
