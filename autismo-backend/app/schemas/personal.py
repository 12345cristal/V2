"""
Schemas de Pydantic para Personal (Terapeutas)
"""

from datetime import date, time
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


# ============= PERSONAL SCHEMAS =============

class PersonalBase(BaseModel):
    usuario_id: int
    especialidad: Optional[str] = None
    certificaciones: Optional[str] = None
    anos_experiencia: Optional[int] = None
    numero_licencia: Optional[str] = None
    estatus: Optional[str] = "ACTIVO"


class PersonalCreate(PersonalBase):
    pass


class PersonalUpdate(BaseModel):
    especialidad: Optional[str] = None
    certificaciones: Optional[str] = None
    anos_experiencia: Optional[int] = None
    numero_licencia: Optional[str] = None
    estatus: Optional[str] = None


class PersonalInDB(PersonalBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class PersonalWithUsuario(PersonalInDB):
    """Personal con datos del usuario asociado"""
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None


# ============= PERSONAL PERFIL SCHEMAS =============

class PersonalPerfilBase(BaseModel):
    personal_id: int
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    grado_academico_id: Optional[int] = None
    estado_laboral_id: Optional[int] = None
    fecha_contratacion: Optional[date] = None


class PersonalPerfilCreate(PersonalPerfilBase):
    pass


class PersonalPerfilUpdate(BaseModel):
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    grado_academico_id: Optional[int] = None
    estado_laboral_id: Optional[int] = None
    fecha_contratacion: Optional[date] = None


class PersonalPerfilInDB(PersonalPerfilBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= PERSONAL HORARIO SCHEMAS =============

class PersonalHorarioBase(BaseModel):
    personal_id: int
    dia_semana: str
    hora_inicio: time
    hora_fin: time


class PersonalHorarioCreate(PersonalHorarioBase):
    pass


class PersonalHorarioUpdate(BaseModel):
    dia_semana: Optional[str] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None


class PersonalHorarioInDB(PersonalHorarioBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= SCHEMAS COMPUESTOS =============

class PersonalCompleto(PersonalWithUsuario):
    """Personal con perfil y horarios incluidos"""
    perfil: Optional[PersonalPerfilInDB] = None
    horarios: List[PersonalHorarioInDB] = []


class PersonalList(BaseModel):
    """Schema mínimo para listados"""
    id: int
    usuario_id: int
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    email: Optional[EmailStr] = None
    especialidad: Optional[str] = None
    anos_experiencia: Optional[int] = None
    estatus: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
