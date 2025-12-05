from pydantic import BaseModel
from datetime import date, datetime

class NinoBase(BaseModel):
    id: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None
    fecha_nacimiento: date
    sexo: str
    estado: str


class NinoCreate(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None
    fecha_nacimiento: date
    sexo: str
    tutor_principal_id: int | None


class DiagnosticoRead(BaseModel):
    diagnostico_principal: str
    diagnostico_resumen: str | None
    fecha_diagnostico: date | None
    especialista: str | None


class EscolarRead(BaseModel):
    escuela: str | None
    grado: str | None
    asiste_escuela: bool


class InfoEmocionalRead(BaseModel):
    estimulos_ansiedad: str | None
    cosas_que_calman: str | None
    preferencias_sensoriales: str | None
    forma_comunicacion: str | None
    nivel_comprension: str


class NinoDetail(NinoBase):
    diagnostico: DiagnosticoRead | None
    escolar: EscolarRead | None
    info_emocional: InfoEmocionalRead | None
