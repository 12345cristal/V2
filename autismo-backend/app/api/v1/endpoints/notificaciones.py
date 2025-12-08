"""
Endpoints para notificaciones
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.usuario import Usuario
from app.schemas.notificacion import NotificacionInDB, NotificacionCreate
from app.services.notificacion_service import notificacion_service


router = APIRouter()


@router.get("/notificaciones/mis-notificaciones")
async def obtener_mis_notificaciones(
    leido: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    """Obtener notificaciones del usuario actual"""
    return notificacion_service.get_notificaciones_usuario(
        db=db,
        usuario_id=current_user.id,
        leido=leido,
        skip=skip,
        limit=limit,
    )


@router.get("/notificaciones/no-leidas/count")
async def contar_no_leidas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    """Contar notificaciones no leídas"""
    count = notificacion_service.count_no_leidas(db=db, usuario_id=current_user.id)
    return {"count": count}


@router.post("/notificaciones/{notificacion_id}/marcar-leida")
async def marcar_leida(
    notificacion_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    """Marcar notificación como leída"""
    return notificacion_service.marcar_leida(db=db, notificacion_id=notificacion_id)


@router.post("/notificaciones/marcar-todas-leidas")
async def marcar_todas_leidas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    """Marcar todas las notificaciones como leídas"""
    return notificacion_service.marcar_todas_leidas(db=db, usuario_id=current_user.id)


@router.delete("/notificaciones/{notificacion_id}")
async def eliminar_notificacion(
    notificacion_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    """Eliminar notificación"""
    return notificacion_service.delete_notificacion(db=db, notificacion_id=notificacion_id)


@router.post("/notificaciones/admin/crear")
async def crear_notificacion_admin(
    notif_data: NotificacionCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("notificaciones:crear")),
):
    """Crear notificación (admin)"""
    return notificacion_service.create_notificacion(db=db, notif_data=notif_data)
