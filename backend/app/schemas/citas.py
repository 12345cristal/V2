from pydantic import BaseModel
from typing import Optional

# ============================
# ESTADOS DE CITA
# ============================
class EstadoCitaSchema(BaseModel):
    id: int
    codigo: str
    nombre: str

class CatalogosCitaResponse(BaseModel):
    estadosCita: list[EstadoCitaSchema]


# ============================
# LISTADO DE CITAS (Angular)
# ============================
class CitaListadoResponse(BaseModel):
    id: int
    nombreNino: str
    tutorNombre: str
    telefonoTutor1: str
    telefonoTutor2: Optional[str]
    fecha: str
    horaInicio: str
    horaFin: str
    estado: str
    esReposicion: bool
    motivo: str
    diagnosticoPresuntivo: Optional[str]
    observaciones: Optional[str]

    class Config:
        from_attributes = True


# ============================
# CREAR CITA (modal)
# ============================
class CitaCrearRequest(BaseModel):
    nombreNino: str
    tutorNombre: str
    telefonoTutor1: str
    telefonoTutor2: Optional[str]

    fecha: str
    horaInicio: str
    duracionMinutos: int

    estadoId: int
    esReposicion: bool
    citaOriginalId: Optional[int]

    motivo: str
    diagnosticoPresuntivo: Optional[str]
    observaciones: Optional[str]


# ============================
# EDITAR CITA
# ============================
class CitaActualizarRequest(CitaCrearRequest):
    id: int
