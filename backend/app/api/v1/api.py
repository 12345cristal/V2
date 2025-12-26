from fastapi import APIRouter
from app.api.v1.endpoints import chat, health

api_router = APIRouter()

# Endpoints de IA y Chat
api_router.include_router(
    chat.router,
    prefix="/ia",
    tags=["IA - Chatbot"]
)

# Health check
api_router.include_router(
    health.router,
    tags=["Salud"]
)
