from pydantic import BaseModel
from datetime import datetime

class AuditoriaRead(BaseModel):
    id: int
    usuario_id: int | None
    accion: str
    tabla_afectada: str | None
    registro_id: int | None
    fecha: datetime
