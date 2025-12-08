"""
Schemas de Pydantic para Tutor (Padres/Tutores)
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


# ============= TUTOR SCHEMAS =============

class TutorBase(BaseModel):
    usuario_id: int
    parentesco: str
    ocupacion: Optional[str] = None
    telefono_emergencia: Optional[str] = None


class TutorCreate(TutorBase):
    pass


class TutorUpdate(BaseModel):
    parentesco: Optional[str] = None
    ocupacion: Optional[str] = None
    telefono_emergencia: Optional[str] = None


class TutorInDB(TutorBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class TutorWithUsuario(TutorInDB):
    """Tutor con datos del usuario asociado"""
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None


# ============= TUTOR DIRECCION SCHEMAS =============

class TutorDireccionBase(BaseModel):
    tutor_id: int
    calle: str
    numero_exterior: str
    numero_interior: Optional[str] = None
    colonia: str
    ciudad: str
    estado: str
    codigo_postal: str
    pais: Optional[str] = "México"


class TutorDireccionCreate(TutorDireccionBase):
    pass


class TutorDireccionUpdate(BaseModel):
    calle: Optional[str] = None
    numero_exterior: Optional[str] = None
    numero_interior: Optional[str] = None
    colonia: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    pais: Optional[str] = None


class TutorDireccionInDB(TutorDireccionBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= SCHEMAS COMPUESTOS =============

class TutorCompleto(TutorWithUsuario):
    """Tutor con dirección incluida"""
    direccion: Optional[TutorDireccionInDB] = None


class TutorList(BaseModel):
    """Schema mínimo para listados"""
    id: int
    usuario_id: int
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    email: Optional[EmailStr] = None
    parentesco: Optional[str] = None
    telefono: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
