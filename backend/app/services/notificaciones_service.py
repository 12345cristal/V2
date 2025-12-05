# app/services/notificaciones_service.py

from sqlalchemy.orm import Session

from app.models.notificaciones import Notificacion


class NotificacionesService:

    @staticmethod
    def obtener(usuario_id: int, db: Session):
        return (
            db.query(Notificacion)
            .filter(Notificacion.usuario_id == usuario_id)
            .order_by(Notificacion.fecha_creacion.desc())
            .all()
        )
