# app/schemas/nino.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


# ============= SUBMODELOS =============

class Direccion(BaseModel):
    calle: Optional[str] = None
    numero: Optional[str] = None
    colonia: Optional[str] = None
    municipio: Optional[str] = None
    codigoPostal: Optional[str] = None


class Diagnostico(BaseModel):
    diagnosticoPrincipal: str
    fechaDiagnostico: Optional[date] = None
    diagnosticosSecundarios: List[str] = []
    especialista: Optional[str] = None
    institucion: Optional[str] = None


class Alergias(BaseModel):
    medicamentos: Optional[str] = None
    alimentos: Optional[str] = None
    ambiental: Optional[str] = None


class MedicamentoActual(BaseModel):
    nombre: str
    dosis: Optional[str] = None
    horario: Optional[str] = None


class Escolar(BaseModel):
    escuela: Optional[str] = None
    grado: Optional[str] = None
    maestro: Optional[str] = None  # no está en BD, se ignora
    horarioClases: Optional[str] = None
    adaptaciones: Optional[str] = None


class ContactoEmergencia(BaseModel):
    nombreCompleto: str
    relacion: str
    telefono: str
    telefonoSecundario: Optional[str] = None
    direccion: Optional[str] = None


class InfoCentro(BaseModel):
    fechaIngreso: Optional[date] = None
    costoMensual: Optional[float] = None  # no BD
    modalidadPago: Optional[str] = None   # no BD
    terapeutaAsignado: Optional[str] = None  # no BD
    horariosTerapia: Optional[str] = None    # no BD
    estado: str = "ACTIVO"


# ============= BASE =============

class NinoBase(BaseModel):
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: Optional[str] = None
    fechaNacimiento: date
    sexo: str = Field(pattern="^(M|F|O)$")
    curp: Optional[str] = None

    direccion: Optional[Direccion] = None
    diagnostico: Optional[Diagnostico] = None
    alergias: Optional[Alergias] = None
    medicamentosActuales: List[MedicamentoActual] = []
    escolar: Optional[Escolar] = None
    contactosEmergencia: List[ContactoEmergencia] = []
    infoCentro: Optional[InfoCentro] = None

    class Config:
        # MUY IMPORTANTE: el front manda MÁS cosas, las ignoramos
        extra = "ignore"


# ============= CREATE / UPDATE =============

class NinoCreate(NinoBase):
    ...


class NinoUpdate(NinoBase):
    id: int


# ============= RESPUESTAS =============

class InfoCentroOut(InfoCentro):
    fechaIngreso: Optional[datetime] = None
    estado: str


class NinoResumen(BaseModel):
    id: int
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: Optional[str] = None
    infoCentro: InfoCentroOut
    progresoGeneral: Optional[float] = 0.0

    class Config:
        orm_mode = True


class NinoDetalle(NinoBase):
    id: int
    edad: Optional[int] = None
    infoCentro: InfoCentroOut
    progresoGeneral: Optional[float] = 0.0

    class Config:
        orm_mode = True
