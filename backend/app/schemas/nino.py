# app/schemas/nino.py
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


# ==================================================
# DIRECCIÓN
# ==================================================
class DireccionBase(BaseModel):
    calle: Optional[str] = None
    numero: Optional[str] = None
    colonia: Optional[str] = None
    municipio: Optional[str] = None
    codigo_postal: Optional[str] = None


class DireccionCreate(DireccionBase):
    pass


class DireccionRead(DireccionBase):
    id: int
    nino_id: int
    
    class Config:
        from_attributes = True


# ==================================================
# DIAGNÓSTICO
# ==================================================
class DiagnosticoBase(BaseModel):
    diagnostico_principal: Optional[str] = None
    diagnostico_resumen: Optional[str] = None
    archivo_url: Optional[str] = None
    fecha_diagnostico: Optional[date] = None
    especialista: Optional[str] = None
    institucion: Optional[str] = None


class DiagnosticoCreate(DiagnosticoBase):
    pass


class DiagnosticoRead(DiagnosticoBase):
    id: int
    nino_id: int
    
    class Config:
        from_attributes = True


# ==================================================
# INFORMACIÓN EMOCIONAL
# ==================================================
class InfoEmocionalBase(BaseModel):
    estimulos: Optional[str] = None
    calmantes: Optional[str] = None
    preferencias: Optional[str] = None
    no_tolera: Optional[str] = None
    palabras_clave: Optional[str] = None
    forma_comunicacion: Optional[str] = None
    nivel_comprension: Optional[str] = "MEDIO"


class InfoEmocionalCreate(InfoEmocionalBase):
    pass


class InfoEmocionalRead(InfoEmocionalBase):
    id: int
    nino_id: int
    
    class Config:
        from_attributes = True


# ==================================================
# ARCHIVOS
# ==================================================
class ArchivosBase(BaseModel):
    acta_url: Optional[str] = None
    curp_url: Optional[str] = None
    comprobante_url: Optional[str] = None
    foto_url: Optional[str] = None
    diagnostico_url: Optional[str] = None
    consentimiento_url: Optional[str] = None
    hoja_ingreso_url: Optional[str] = None


class ArchivosCreate(ArchivosBase):
    pass


class ArchivosRead(ArchivosBase):
    id: int
    nino_id: int
    
    class Config:
        from_attributes = True


# ==================================================
# NIÑO (Principal)
# ==================================================
class NinoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido_paterno: str = Field(..., min_length=1, max_length=60)
    apellido_materno: Optional[str] = Field(None, max_length=60)
    fecha_nacimiento: date
    sexo: str = Field(..., pattern="^(M|F|O)$")
    curp: Optional[str] = Field(None, max_length=18)
    tutor_id: Optional[int] = None
    estado: Optional[str] = Field("ACTIVO", pattern="^(ACTIVO|INACTIVO)$")


class NinoCreate(NinoBase):
    # Datos adicionales opcionales al crear
    direccion: Optional[DireccionCreate] = None
    diagnostico: Optional[DiagnosticoCreate] = None
    info_emocional: Optional[InfoEmocionalCreate] = None
    archivos: Optional[ArchivosCreate] = None


class NinoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido_paterno: Optional[str] = Field(None, min_length=1, max_length=60)
    apellido_materno: Optional[str] = Field(None, max_length=60)
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = Field(None, pattern="^(M|F|O)$")
    curp: Optional[str] = Field(None, max_length=18)
    tutor_id: Optional[int] = None
    estado: Optional[str] = Field(None, pattern="^(ACTIVO|INACTIVO)$")
    
    # Datos adicionales
    direccion: Optional[DireccionCreate] = None
    diagnostico: Optional[DiagnosticoCreate] = None
    info_emocional: Optional[InfoEmocionalCreate] = None
    archivos: Optional[ArchivosCreate] = None


class NinoRead(NinoBase):
    id: int
    fecha_registro: datetime
    
    class Config:
        from_attributes = True


class NinoDetalle(NinoRead):
    """Niño con todos sus datos relacionados"""
    direccion: Optional[DireccionRead] = None
    diagnostico: Optional[DiagnosticoRead] = None
    info_emocional: Optional[InfoEmocionalRead] = None
    archivos: Optional[ArchivosRead] = None
    tutor_nombre: Optional[str] = None  # Nombre completo del tutor
    
    class Config:
        from_attributes = True


# ==================================================
# LISTA CON PAGINACIÓN
# ==================================================
class NinoListItem(BaseModel):
    """Información resumida del niño para listados"""
    id: int
    nombre: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    edad: Optional[int] = None  # Calculada
    sexo: str
    estado: str
    tutor_nombre: Optional[str] = None
    foto_url: Optional[str] = None
    
    class Config:
        from_attributes = True


# Alias para mantener compatibilidad con el router
NinoListResponse = NinoListItem


# Alias para NinoResponse (respuesta completa)
NinoResponse = NinoDetalle
