# app/api/v1/endpoints/padre/notificaciones.py
"""
Router para Notificaciones desde el módulo Padre
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db_session, require_padre
from app.models.usuario import Usuario
from app.models.tutor import Tutor
from app.schemas.padre import Notificacion, NotificacionesListResponse


router = APIRouter()


@router.get("/notificaciones/{padre_id}", response_model=List[Notificacion])
async def listar_notificaciones(
    padre_id: int,
    leidas: Optional[bool] = Query(None, description="Filtrar por leídas/no leídas"),
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Lista notificaciones del padre con filtro opcional
    """
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    # TODO: Implementar modelo de notificaciones y lógica real
    return []


@router.put("/notificaciones/{notificacion_id}/leida")
async def marcar_notificacion_leida(
    notificacion_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Marca notificación como leída
    """
    # TODO: Verificar permisos y actualizar notificación
    return {"message": "Notificación marcada como leída"}


@router.delete("/notificaciones/{notificacion_id}")
async def eliminar_notificacion(
    notificacion_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Elimina una notificación
    """
    # TODO: Verificar permisos y eliminar notificación
    return {"message": "Notificación eliminada"}
