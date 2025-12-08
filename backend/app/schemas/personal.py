# backend/app/schemas/personal.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date, time
from app.models.personal import EstadoLaboral


# ========== HORARIOS ==========
class HorarioCreate(BaseModel):
    id_personal: int
    dia_semana: int = Field(..., ge=1, le=7, description="1=Lunes, 7=Domingo")
    hora_inicio: time
    hora_fin: time
    
    @field_validator('hora_fin')
    @classmethod
    def validate_hora_fin(cls, v, info):
        if 'hora_inicio' in info.data and v <= info.data['hora_inicio']:
            raise ValueError('hora_fin debe ser mayor que hora_inicio')
        return v


class HorarioUpdate(BaseModel):
    dia_semana: Optional[int] = Field(None, ge=1, le=7)
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None


class HorarioResponse(BaseModel):
    id_horario: int = Field(validation_alias="id", serialization_alias="id_horario")
    id_personal: int
    dia_semana: int
    hora_inicio: time
    hora_fin: time
    
    class Config:
        from_attributes = True
        populate_by_name = True


# ========== PERSONAL ==========
class PersonalBase(BaseModel):
    nombres: str = Field(..., min_length=1, max_length=100)
    apellido_paterno: str = Field(..., min_length=1, max_length=100)
    apellido_materno: Optional[str] = Field(None, max_length=100)
    id_rol: int
    rfc: str = Field(..., min_length=13, max_length=13)
    curp: str = Field(..., min_length=18, max_length=18)
    fecha_nacimiento: date
    telefono_personal: str = Field(..., min_length=10, max_length=10)
    correo_personal: str = Field(..., max_length=150)
    especialidad_principal: Optional[str] = Field(None, max_length=100)
    especialidades: Optional[str] = Field(None, max_length=500)
    grado_academico: Optional[str] = Field(None, max_length=100)
    cedula_profesional: Optional[str] = Field(None, max_length=20)
    fecha_ingreso: date
    experiencia: Optional[int] = Field(0, ge=0)
    
    # Domicilio
    calle: Optional[str] = Field(None, max_length=200)
    numero_exterior: Optional[str] = Field(None, max_length=10)
    numero_interior: Optional[str] = Field(None, max_length=10)
    colonia: Optional[str] = Field(None, max_length=100)
    ciudad: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=5)


class PersonalCreate(PersonalBase):
    pass


class PersonalUpdate(BaseModel):
    nombres: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido_paterno: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido_materno: Optional[str] = Field(None, max_length=100)
    id_rol: Optional[int] = None
    rfc: Optional[str] = Field(None, min_length=13, max_length=13)
    curp: Optional[str] = Field(None, min_length=18, max_length=18)
    fecha_nacimiento: Optional[date] = None
    telefono_personal: Optional[str] = Field(None, min_length=10, max_length=10)
    correo_personal: Optional[str] = Field(None, max_length=150)
    especialidad_principal: Optional[str] = Field(None, max_length=100)
    especialidades: Optional[str] = Field(None, max_length=500)
    grado_academico: Optional[str] = Field(None, max_length=100)
    cedula_profesional: Optional[str] = Field(None, max_length=20)
    experiencia: Optional[int] = Field(None, ge=0)
    
    # Domicilio
    calle: Optional[str] = Field(None, max_length=200)
    numero_exterior: Optional[str] = Field(None, max_length=10)
    numero_interior: Optional[str] = Field(None, max_length=10)
    colonia: Optional[str] = Field(None, max_length=100)
    ciudad: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=5)


class PersonalResponse(BaseModel):
    id_personal: int = Field(validation_alias="id", serialization_alias="id_personal")
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    id_rol: int
    rfc: str
    curp: str
    fecha_nacimiento: date
    telefono_personal: str
    correo_personal: str
    especialidad_principal: Optional[str]
    especialidades: Optional[str]
    grado_academico: Optional[str]
    cedula_profesional: Optional[str]
    fecha_ingreso: date
    experiencia: int
    estado_laboral: EstadoLaboral
    total_pacientes: int
    sesiones_semana: int
    rating: int
    
    # Domicilio con aliases para el frontend
    domicilio_calle: Optional[str] = Field(None, validation_alias="calle", serialization_alias="domicilio_calle")
    domicilio_colonia: Optional[str] = Field(None, validation_alias="colonia", serialization_alias="domicilio_colonia")
    domicilio_cp: Optional[str] = Field(None, validation_alias="codigo_postal", serialization_alias="domicilio_cp")
    domicilio_municipio: Optional[str] = Field(None, validation_alias="ciudad", serialization_alias="domicilio_municipio")
    domicilio_estado: Optional[str] = Field(None, validation_alias="estado", serialization_alias="domicilio_estado")
    numero_exterior: Optional[str] = None
    numero_interior: Optional[str] = None
    
    # Otros campos (no están en la BD pero los agrega el frontend con defaults)
    ine: Optional[str] = None
    cv_archivo: Optional[str] = None
    foto_url: Optional[str] = None
    
    horarios: List[HorarioResponse] = []
    
    class Config:
        from_attributes = True
        populate_by_name = True


class PersonalListItem(BaseModel):
    id_personal: int = Field(validation_alias="id", serialization_alias="id_personal")
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    id_rol: int
    especialidad_principal: Optional[str]
    especialidades: Optional[str]
    grado_academico: Optional[str]
    telefono_personal: str
    correo_personal: str
    fecha_ingreso: date
    fecha_nacimiento: date
    estado_laboral: EstadoLaboral
    experiencia: int
    total_pacientes: int
    sesiones_semana: int
    rating: int
    rfc: str
    curp: str
    domicilio_calle: Optional[str] = Field(None, validation_alias="calle", serialization_alias="domicilio_calle")
    domicilio_colonia: Optional[str] = Field(None, validation_alias="colonia", serialization_alias="domicilio_colonia")
    domicilio_cp: Optional[str] = Field(None, validation_alias="codigo_postal", serialization_alias="domicilio_cp")
    domicilio_municipio: Optional[str] = Field(None, validation_alias="ciudad", serialization_alias="domicilio_municipio")
    domicilio_estado: Optional[str] = Field(None, validation_alias="estado", serialization_alias="domicilio_estado")
    
    # Campos opcionales que no siempre están en la respuesta de lista
    ine: Optional[str] = None
    cv_archivo: Optional[str] = None
    foto_url: Optional[str] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True


class PersonalListResponse(BaseModel):
    items: List[PersonalListItem]
    total: int
    page: int
    page_size: int
    total_pages: int
