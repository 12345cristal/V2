# app/schemas/perfil.py
from pydantic import BaseModel
from typing import Optional
from app.models.usuario import Usuario
from app.models.personal import Personal
from app.models.personal_perfil import PersonalPerfil


class PerfilResponse(BaseModel):
    id_personal: int

    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]

    fecha_nacimiento: Optional[str]

    telefono_personal: Optional[str]
    correo_personal: Optional[str]

    grado_academico: Optional[str]
    especialidad_principal: Optional[str]
    especialidades: Optional[str]
    experiencia: Optional[str]

    domicilio_calle: Optional[str]
    domicilio_colonia: Optional[str]
    domicilio_cp: Optional[str]
    domicilio_municipio: Optional[str]
    domicilio_estado: Optional[str]

    foto_perfil: Optional[str]
    cv_archivo: Optional[str]

    fecha_ingreso: Optional[str]
    estado_laboral: Optional[str]
    total_pacientes: Optional[int]
    sesiones_semana: Optional[int]
    rating: Optional[float]

    class Config:
        from_attributes = True

    @staticmethod
    def from_db(personal: Personal, perfil: PersonalPerfil, user: Usuario):
        return PerfilResponse(
            id_personal=personal.id,

            nombres=personal.nombres,
            apellido_paterno=personal.apellido_paterno,
            apellido_materno=personal.apellido_materno,

            fecha_nacimiento=str(personal.fecha_nacimiento) if personal.fecha_nacimiento else None,

            telefono_personal=perfil.telefono_personal or personal.telefono_personal,
            correo_personal=perfil.correo_personal or personal.correo_personal,

            grado_academico=personal.grado_academico,
            especialidad_principal=personal.especialidad_principal,
            especialidades=perfil.especialidades or personal.especialidades,
            experiencia=perfil.experiencia or personal.experiencia,

            domicilio_calle=perfil.domicilio_calle or personal.calle,
            domicilio_colonia=perfil.domicilio_colonia or personal.colonia,
            domicilio_cp=perfil.domicilio_cp or personal.codigo_postal,
            domicilio_municipio=perfil.domicilio_municipio or personal.ciudad,
            domicilio_estado=perfil.domicilio_estado or personal.estado,

            foto_perfil=perfil.foto_url or personal.foto_perfil,
            cv_archivo=perfil.cv_url or personal.cv_archivo,

            fecha_ingreso=str(personal.fecha_ingreso) if personal.fecha_ingreso else None,
            estado_laboral=str(personal.estado_laboral.value) if personal.estado_laboral else None,
            total_pacientes=personal.total_pacientes,
            sesiones_semana=personal.sesiones_semana,
            rating=personal.rating,
        )
