# app/api/v1/endpoints/padre/mensajes.py
"""
Router para Mensajes y Chat desde el módulo Padre
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db_session, require_padre
from app.models.usuario import Usuario
from app.models.tutor import Tutor
from app.schemas.padre import Mensaje, MensajeCreate, ChatResumen, MensajesListResponse


router = APIRouter()


@router.get("/chats/{padre_id}", response_model=List[ChatResumen])
async def listar_chats(
    padre_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Lista chats activos del padre
    """
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    # TODO: Implementar modelo de chat y lógica real
    return []


@router.get("/chats/{chat_id}/mensajes", response_model=List[Mensaje])
async def obtener_mensajes(
    chat_id: int,
    limite: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene historial de mensajes de un chat
    """
    # TODO: Verificar que el padre tenga acceso al chat
    # TODO: Implementar lógica real
    return []


@router.post("/chats/{chat_id}/mensajes")
async def enviar_mensaje(
    chat_id: int,
    mensaje: MensajeCreate,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Envía un mensaje (texto/audio/archivo)
    """
    # TODO: Verificar que el padre tenga acceso al chat
    # TODO: Implementar lógica de envío de mensaje
    return {"message": "Mensaje enviado", "chat_id": chat_id}


@router.get("/chats/{chat_id}/mensajes/{mensaje_id}", response_model=Mensaje)
async def obtener_detalle_mensaje(
    chat_id: int,
    mensaje_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene detalle de un mensaje específico
    """
    # TODO: Implementar lógica real
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Mensaje no encontrado"
    )
