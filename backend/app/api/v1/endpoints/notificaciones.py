# app/api/v1/endpoints/notificaciones.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.notificacion import Notificacion
from app.schemas.notificacion import NotificacionCreate, NotificacionRead
from app.models.usuario import Usuario

router = APIRouter(
    prefix="/notificaciones",
    tags=["notificaciones"],
)


@router.get("/", response_model=List[NotificacionRead])
def list_my_notifications(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
    solo_no_leidas: bool = Query(False),
):
    query = db.query(Notificacion).filter(
        Notificacion.usuario_id == current_user.id
    )
    if solo_no_leidas:
        query = query.filter(Notificacion.leida.is_(False))

    notifs = query.order_by(Notificacion.fecha_creacion.desc()).all()
    return notifs


@router.post("/", response_model=NotificacionRead, status_code=status.HTTP_201_CREATED)
def create_notification(
    data: NotificacionCreate,
    db: Session = Depends(get_db),
):
    notif = Notificacion(**data.model_dump())
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


@router.post("/{notif_id}/leer", response_model=NotificacionRead)
def mark_notification_as_read(
    notif_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    notif = db.get(Notificacion, notif_id)
    if not notif or notif.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada",
        )
    notif.leida = True
    db.commit()
    db.refresh(notif)
    return notif
