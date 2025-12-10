# app/schemas/ficha_emergencia.py
"""
Schemas para Fichas de Emergencia
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FichaEmergenciaBase(BaseModel):
    """Base para ficha de emergencia"""
    tipo_sangre: Optional[str] = Field(None, max_length=10)
    alergias: Optional[str] = None
    condiciones_medicas: Optional[str] = None
    medicamentos_actuales: Optional[str] = None
    diagnostico_principal: Optional[str] = Field(None, max_length=255)
    diagnostico_detallado: Optional[str] = None
    
    # Contacto principal
    contacto_principal_nombre: str = Field(..., max_length=200)
    contacto_principal_relacion: Optional[str] = Field(None, max_length=100)
    contacto_principal_telefono: str = Field(..., max_length=20)
    contacto_principal_telefono_alt: Optional[str] = Field(None, max_length=20)
    
    # Contacto secundario
    contacto_secundario_nombre: Optional[str] = Field(None, max_length=200)
    contacto_secundario_relacion: Optional[str] = Field(None, max_length=100)
    contacto_secundario_telefono: Optional[str] = Field(None, max_length=20)
    
    # Información médica
    seguro_medico: Optional[str] = Field(None, max_length=200)
    numero_seguro: Optional[str] = Field(None, max_length=100)
    hospital_preferido: Optional[str] = Field(None, max_length=255)
    medico_tratante: Optional[str] = Field(None, max_length=200)
    telefono_medico: Optional[str] = Field(None, max_length=20)
    
    # Instrucciones
    instrucciones_emergencia: Optional[str] = None
    restricciones_alimenticias: Optional[str] = None
    
    # Comportamiento
    crisis_comunes: Optional[str] = None
    como_calmar: Optional[str] = None
    trigger_points: Optional[str] = None


class FichaEmergenciaCreate(FichaEmergenciaBase):
    """Schema para crear ficha de emergencia"""
    nino_id: int


class FichaEmergenciaUpdate(FichaEmergenciaBase):
    """Schema para actualizar ficha de emergencia"""
    contacto_principal_nombre: Optional[str] = Field(None, max_length=200)
    contacto_principal_telefono: Optional[str] = Field(None, max_length=20)


class FichaEmergenciaResponse(FichaEmergenciaBase):
    """Schema de respuesta de ficha de emergencia"""
    id: int
    nino_id: int
    activa: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    # Información del niño
    nino_nombre_completo: Optional[str] = None
    nino_foto_url: Optional[str] = None
    nino_edad: Optional[int] = None
    nino_estado: Optional[str] = None
    
    class Config:
        from_attributes = True


class FichaEmergenciaImprimible(BaseModel):
    """Schema para impresión de ficha de emergencia"""
    # Datos del niño
    nino_nombre_completo: str
    nino_foto_url: Optional[str] = None
    nino_fecha_nacimiento: Optional[str] = None
    nino_edad: Optional[int] = None
    nino_sexo: Optional[str] = None
    
    # Información médica crítica
    tipo_sangre: Optional[str] = None
    alergias: Optional[str] = None
    diagnostico_principal: Optional[str] = None
    medicamentos_actuales: Optional[str] = None
    
    # Contactos de emergencia
    contacto_principal_nombre: str
    contacto_principal_relacion: Optional[str] = None
    contacto_principal_telefono: str
    contacto_principal_telefono_alt: Optional[str] = None
    contacto_secundario_nombre: Optional[str] = None
    contacto_secundario_telefono: Optional[str] = None
    
    # Información médica
    seguro_medico: Optional[str] = None
    hospital_preferido: Optional[str] = None
    medico_tratante: Optional[str] = None
    
    # Instrucciones
    instrucciones_emergencia: Optional[str] = None
    crisis_comunes: Optional[str] = None
    como_calmar: Optional[str] = None
    
    fecha_generacion: datetime = Field(default_factory=datetime.utcnow)
