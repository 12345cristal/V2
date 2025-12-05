from pydantic import BaseModel
from datetime import datetime

class PerfilPersonalRead(BaseModel):
    grado_academico_id: int | None
    especialidad_principal: str | None
    especialidades: str | None
    experiencia: str | None
    fecha_ingreso: datetime | None
    total_pacientes: int | None
    sesiones_semana: int | None
    rating: str | None


class PersonalBase(BaseModel):
    id: int
    usuario_id: int
    cedula_profesional: str | None
    especialidad: str | None
    anio_experiencia: int | None


class PersonalRead(PersonalBase):
    perfil: PerfilPersonalRead | None
