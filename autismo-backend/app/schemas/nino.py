"""
Schemas de Pydantic para Niño y entidades relacionadas
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# ============= NINO SCHEMAS =============

class NinoBase(BaseModel):
    tutor_id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    fecha_nacimiento: date
    sexo: str
    curp: Optional[str] = None
    nss: Optional[str] = None
    foto_url: Optional[str] = None


class NinoCreate(NinoBase):
    pass


class NinoUpdate(BaseModel):
    tutor_id: Optional[int] = None
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = None
    curp: Optional[str] = None
    nss: Optional[str] = None
    foto_url: Optional[str] = None


class NinoInDB(NinoBase):
    id: int
    fecha_registro: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============= NINO DIRECCION SCHEMAS =============

class NinoDireccionBase(BaseModel):
    nino_id: int
    calle: str
    numero_exterior: str
    numero_interior: Optional[str] = None
    colonia: str
    ciudad: str
    estado: str
    codigo_postal: str
    pais: Optional[str] = "México"


class NinoDireccionCreate(NinoDireccionBase):
    pass


class NinoDireccionUpdate(BaseModel):
    calle: Optional[str] = None
    numero_exterior: Optional[str] = None
    numero_interior: Optional[str] = None
    colonia: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    pais: Optional[str] = None


class NinoDireccionInDB(NinoDireccionBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= NINO DIAGNOSTICO SCHEMAS =============

class NinoDiagnosticoBase(BaseModel):
    nino_id: int
    diagnostico_principal: str
    diagnostico_secundario: Optional[str] = None
    fecha_diagnostico: Optional[date] = None
    medico_diagnostico: Optional[str] = None
    observaciones: Optional[str] = None


class NinoDiagnosticoCreate(NinoDiagnosticoBase):
    pass


class NinoDiagnosticoUpdate(BaseModel):
    diagnostico_principal: Optional[str] = None
    diagnostico_secundario: Optional[str] = None
    fecha_diagnostico: Optional[date] = None
    medico_diagnostico: Optional[str] = None
    observaciones: Optional[str] = None


class NinoDiagnosticoInDB(NinoDiagnosticoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= NINO INFO EMOCIONAL SCHEMAS =============

class NinoInfoEmocionalBase(BaseModel):
    nino_id: int
    temperamento: Optional[str] = None
    intereses: Optional[str] = None
    miedos: Optional[str] = None
    conductas_desafiantes: Optional[str] = None
    motivadores: Optional[str] = None
    estrategias_calmado: Optional[str] = None


class NinoInfoEmocionalCreate(NinoInfoEmocionalBase):
    pass


class NinoInfoEmocionalUpdate(BaseModel):
    temperamento: Optional[str] = None
    intereses: Optional[str] = None
    miedos: Optional[str] = None
    conductas_desafiantes: Optional[str] = None
    motivadores: Optional[str] = None
    estrategias_calmado: Optional[str] = None


class NinoInfoEmocionalInDB(NinoInfoEmocionalBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= NINO ARCHIVOS SCHEMAS =============

class NinoArchivosBase(BaseModel):
    nino_id: int
    tipo_archivo: str
    nombre_archivo: str
    url_archivo: str
    descripcion: Optional[str] = None


class NinoArchivosCreate(NinoArchivosBase):
    pass


class NinoArchivosUpdate(BaseModel):
    tipo_archivo: Optional[str] = None
    nombre_archivo: Optional[str] = None
    url_archivo: Optional[str] = None
    descripcion: Optional[str] = None


class NinoArchivosInDB(NinoArchivosBase):
    id: int
    fecha_subida: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============= SCHEMAS COMPUESTOS =============

class NinoCompleto(NinoInDB):
    """Niño con toda la información relacionada"""
    direccion: Optional[NinoDireccionInDB] = None
    diagnostico: Optional[NinoDiagnosticoInDB] = None
    info_emocional: Optional[NinoInfoEmocionalInDB] = None
    archivos: List[NinoArchivosInDB] = []
    tutor_nombre: Optional[str] = None


class NinoList(BaseModel):
    """Schema mínimo para listados"""
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    fecha_nacimiento: date
    sexo: str
    tutor_nombre: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
