# app/schemas/personal.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from app.models.personal import EstadoLaboralEnum


class HorarioPersonalBase(BaseModel):
    dia_semana: int
    hora_inicio: str
    hora_fin: str


class HorarioPersonalRead(HorarioPersonalBase):
    id_horario: int

    class Config:
        from_attributes = True


class PersonalBase(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    id_rol: int
    especialidad_principal: str

    telefono_personal: str
    correo_personal: EmailStr

    fecha_ingreso: date
    estado_laboral: EstadoLaboralEnum = EstadoLaboralEnum.ACTIVO

    total_pacientes: Optional[int] = None
    sesiones_semana: Optional[int] = None
    rating: Optional[int] = None

    fecha_nacimiento: date
    grado_academico: str
    especialidades: str
    rfc: str
    ine: str
    curp: str

    domicilio_calle: str
    domicilio_colonia: str
    domicilio_cp: str
    domicilio_municipio: str
    domicilio_estado: str

    cv_archivo: Optional[str] = None
    experiencia: str


class PersonalCreate(PersonalBase):
    horarios: Optional[List[HorarioPersonalBase]] = None


class PersonalUpdate(BaseModel):
    # aquí todo opcional para PATCH/PUT
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    id_rol: Optional[int] = None
    especialidad_principal: Optional[str] = None
    telefono_personal: Optional[str] = None
    correo_personal: Optional[EmailStr] = None
    fecha_ingreso: Optional[date] = None
    estado_laboral: Optional[EstadoLaboralEnum] = None
    total_pacientes: Optional[int] = None
    sesiones_semana: Optional[int] = None
    rating: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    grado_academico: Optional[str] = None
    especialidades: Optional[str] = None
    rfc: Optional[str] = None
    ine: Optional[str] = None
    curp: Optional[str] = None
    domicilio_calle: Optional[str] = None
    domicilio_colonia: Optional[str] = None
    domicilio_cp: Optional[str] = None
    domicilio_municipio: Optional[str] = None
    domicilio_estado: Optional[str] = None
    cv_archivo: Optional[str] = None
    experiencia: Optional[str] = None
    horarios: Optional[List[HorarioPersonalBase]] = None


class PersonalRead(PersonalBase):
    id_personal: int
    horarios: List[HorarioPersonalRead] = []

    class Config:
        from_attributes = True
