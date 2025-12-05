from pydantic import BaseModel
from datetime import datetime

class NotificacionRead(BaseModel):
    id: int
    titulo: str
    mensaje: str
    tipo: str
    leida: bool
    fecha_creacion: datetime
