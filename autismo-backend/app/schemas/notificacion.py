"""
Schemas de Pydantic para Notificación
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# ============= NOTIFICACION SCHEMAS =============

class NotificacionBase(BaseModel):
    usuario_id: int
    tipo: str
    titulo: str
    mensaje: str
    leida: Optional[int] = 0


class NotificacionCreate(NotificacionBase):
    pass


class NotificacionUpdate(BaseModel):
    leida: Optional[int] = None


class NotificacionInDB(NotificacionBase):
    id: int
    fecha_envio: datetime
    
    model_config = ConfigDict(from_attributes=True)


class NotificacionList(BaseModel):
    """Schema para listados"""
    id: int
    tipo: str
    titulo: str
    mensaje: str
    leida: int
    fecha_envio: datetime
    
    model_config = ConfigDict(from_attributes=True)


class NotificacionCreateBulk(BaseModel):
    """Schema para crear notificaciones masivas"""
    usuario_ids: list[int]
    tipo: str
    titulo: str
    mensaje: str
