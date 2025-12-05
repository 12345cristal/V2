from pydantic import BaseModel
from datetime import date, time

class CitaRead(BaseModel):
    id: int
    nino_id: int | None
    terapeuta_id: int | None
    terapia_id: int | None
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado_id: int
    es_reposicion: bool
    motivo: str | None


class CrearCita(BaseModel):
    nino_id: int | None
    terapeuta_id: int
    terapia_id: int | None
    fecha: date
    hora_inicio: time
    hora_fin: time
    motivo: str | None
