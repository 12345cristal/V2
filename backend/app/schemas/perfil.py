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

            # 🔥 CORREGIDO: datos reales del usuario
            nombres=user.nombres,
            apellido_paterno=user.apellido_paterno,
            apellido_materno=user.apellido_materno,

            fecha_nacimiento=str(perfil.fecha_nacimiento) if perfil.fecha_nacimiento else None,

            telefono_personal=perfil.telefono_personal,
            correo_personal=perfil.correo_personal,

            grado_academico=None,  # Si luego cargas catálogo
            especialidades=perfil.especialidades,
            experiencia=perfil.experiencia,
            especialidad_principal=personal.especialidad_principal,

            domicilio_calle=perfil.domicilio_calle,
            domicilio_colonia=perfil.domicilio_colonia,
            domicilio_cp=perfil.domicilio_cp,
            domicilio_municipio=perfil.domicilio_municipio,
            domicilio_estado=perfil.domicilio_estado,

            foto_perfil=perfil.foto_url,
            cv_archivo=perfil.cv_url,

            fecha_ingreso=str(personal.fecha_ingreso) if personal.fecha_ingreso else None,
            estado_laboral=str(personal.estado_laboral) if personal.estado_laboral else None,
            total_pacientes=personal.total_pacientes,
            sesiones_semana=personal.sesiones_semana,
            rating=personal.rating
        )
