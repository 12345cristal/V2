from pydantic import BaseModel, field_validator
from typing import Optional, Literal


class RegistrarAsistencia(BaseModel):
    id_sesion: int
    estado: Literal['asistio', 'cancelada', 'reprogramada']
    fecha_registro: str
    nota: Optional[str] = None


class ReprogramarSesion(BaseModel):
    id_sesion: int
    nueva_fecha: str
    nueva_hora: str
    motivo: str


class EnviarMensaje(BaseModel):
    tipo_destinatario: str
    id_destinatario: int
    mensaje: str
