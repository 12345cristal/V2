"""
Notificacion Service - Lógica de negocio para notificaciones
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models.notificacion import Notificacion
from app.models.usuario import Usuario
from app.schemas.notificacion import NotificacionCreate


class NotificacionService:
    """Servicio para gestión de notificaciones"""
    
    @staticmethod
    def get_notificaciones_usuario(
        db: Session,
        usuario_id: int,
        leido: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Notificacion]:
        """Obtener notificaciones de un usuario"""
        query = (
            db.query(Notificacion)
            .options(joinedload(Notificacion.usuario))
            .filter(Notificacion.usuario_id == usuario_id)
        )
        
        if leido is not None:
            query = query.filter(Notificacion.leido == (1 if leido else 0))
        
        return query.order_by(Notificacion.fecha_creacion.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_notificacion(db: Session, notif_data: NotificacionCreate) -> Notificacion:
        """Crear nueva notificación"""
        usuario = db.query(Usuario).filter(Usuario.id == notif_data.usuario_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {notif_data.usuario_id} no encontrado",
            )
        
        notificacion = Notificacion(**notif_data.model_dump())
        db.add(notificacion)
        db.commit()
        db.refresh(notificacion)
        return notificacion
    
    @staticmethod
    def marcar_leida(db: Session, notificacion_id: int) -> Notificacion:
        """Marcar notificación como leída"""
        notificacion = db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()
        
        if not notificacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notificación con ID {notificacion_id} no encontrada",
            )
        
        notificacion.leido = 1
        db.commit()
        db.refresh(notificacion)
        return notificacion
    
    @staticmethod
    def marcar_todas_leidas(db: Session, usuario_id: int) -> dict:
        """Marcar todas las notificaciones de un usuario como leídas"""
        count = (
            db.query(Notificacion)
            .filter(Notificacion.usuario_id == usuario_id, Notificacion.leido == 0)
            .update({"leido": 1})
        )
        
        db.commit()
        return {"message": f"{count} notificaciones marcadas como leídas"}
    
    @staticmethod
    def count_no_leidas(db: Session, usuario_id: int) -> int:
        """Contar notificaciones no leídas"""
        return (
            db.query(Notificacion)
            .filter(Notificacion.usuario_id == usuario_id, Notificacion.leido == 0)
            .count()
        )
    
    @staticmethod
    def delete_notificacion(db: Session, notificacion_id: int) -> dict:
        """Eliminar notificación"""
        notificacion = db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()
        
        if not notificacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notificación con ID {notificacion_id} no encontrada",
            )
        
        db.delete(notificacion)
        db.commit()
        return {"message": "Notificación eliminada exitosamente"}


# Instancia global del servicio
notificacion_service = NotificacionService()
