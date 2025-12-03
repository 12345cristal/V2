# app/schemas/notificacion.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NotificacionBase(BaseModel):
    titulo: str | None = None
    mensaje: str | None = None
    tipo: str  # 'cambio-horario', 'reposicion', 'documento', 'alerta'


class NotificacionCreate(NotificacionBase):
    usuario_id: int


class NotificacionRead(NotificacionBase):
    id: int
    usuario_id: int
    leida: bool
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)
