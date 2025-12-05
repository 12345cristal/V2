from pydantic import BaseModel
from typing import Optional, List


# ==========================================
# SUB-SCHEMAS
# ==========================================

class DireccionSchema(BaseModel):
    calle: Optional[str]
    numero: Optional[str]
    colonia: Optional[str]
    municipio: Optional[str]
    codigoPostal: Optional[str]


class DiagnosticoSchema(BaseModel):
    diagnosticoPrincipal: str
    fechaDiagnostico: Optional[str]
    diagnosticosSecundarios: List[str] = []
    especialista: Optional[str]
    institucion: Optional[str]


class AlergiasSchema(BaseModel):
    medicamentos: Optional[str]
    alimentos: Optional[str]
    ambiental: Optional[str]


class MedicamentoSchema(BaseModel):
    nombre: str
    dosis: Optional[str]
    horario: Optional[str]


class EscolarSchema(BaseModel):
    escuela: Optional[str]
    grado: Optional[str]
    maestro: Optional[str]
    horarioClases: Optional[str]
    adaptaciones: Optional[str]


class TutorInfoSchema(BaseModel):
    nombreCompleto: str
    telefono: Optional[str]
    telefonoSecundario: Optional[str]
    correo: Optional[str]
    ocupacion: Optional[str]
    direccionLaboral: Optional[str]


class ContactoEmergenciaSchema(BaseModel):
    nombreCompleto: str
    relacion: str
    telefono: str
    telefonoSecundario: Optional[str]


class TerapiasCentroSchema(BaseModel):
    lenguaje: bool
    conductual: bool
    ocupacional: bool
    sensorial: bool
    psicologia: bool


class InfoCentroSchema(BaseModel):
    fechaIngreso: str
    costoMensual: Optional[float]
    modalidadPago: Optional[str]
    terapeutaAsignado: Optional[str]
    horariosTerapia: Optional[str]
    estado: str
    terapias: TerapiasCentroSchema


# ==========================================
# NIÑO COMPLETO (detalle para editar)
# ==========================================

class NinoDetalle(BaseModel):
    id: int
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str
    fechaNacimiento: str
    edad: int
    sexo: str
    curp: Optional[str]

    direccion: DireccionSchema
    diagnostico: DiagnosticoSchema
    alergias: AlergiasSchema
    medicamentosActuales: List[MedicamentoSchema]
    escolar: EscolarSchema

    padre: TutorInfoSchema
    madre: TutorInfoSchema
    tutorLegal: TutorInfoSchema
    contactosEmergencia: List[ContactoEmergenciaSchema]

    infoCentro: InfoCentroSchema

    progresoGeneral: Optional[int] = 0

    class Config:
        from_attributes = True


# ==========================================
# LISTADO GENERAL — usado por ninos.ts
# ==========================================

class NinoListado(BaseModel):
    id: int
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str
    infoCentro: InfoCentroSchema
    progresoGeneral: Optional[int]

    class Config:
        from_attributes = True


# ==========================================
# REQUEST PARA CREAR / EDITAR NIÑO
# ==========================================

class NinoCreateRequest(BaseModel):
    nino: dict   # Angular envía JSON crudo
    # Archivos no se declaran aquí → se reciben por FormData

class NinoUpdateRequest(NinoCreateRequest):
    pass
