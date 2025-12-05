from pydantic import BaseModel
from datetime import datetime

class TerapiaBase(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    duracion_minutos: int


class SesionTerapiaRead(BaseModel):
    id: int
    fecha_sesion: datetime
    asistio: bool
    nivel_progreso: int
    nivel_colaboracion: int
    observaciones: str | None


class TerapiaAsignada(BaseModel):
    id: int
    terapia_id: int
    nino_id: int
    terapeuta_id: int | None
    fecha_asignacion: datetime
    frecuencia_semana: int
    prioridad_id: int
    activo: bool
