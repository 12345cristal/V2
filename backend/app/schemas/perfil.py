# app/schemas/perfil.py
from pydantic import BaseModel
from typing import Optional, List
from app.models.usuario import Usuario
from app.models.personal import Personal
from app.models.personal_perfil import PersonalPerfil
import json


class PerfilResponse(BaseModel):
    id_personal: int

    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None

    fecha_nacimiento: Optional[str] = None

    telefono_personal: Optional[str] = None
    correo_personal: Optional[str] = None

    grado_academico: Optional[str] = None
    especialidad_principal: Optional[str] = None
    especialidades: Optional[str] = None
    experiencia: Optional[str] = None

    domicilio_calle: Optional[str] = None
    domicilio_colonia: Optional[str] = None
    domicilio_cp: Optional[str] = None
    domicilio_municipio: Optional[str] = None
    domicilio_estado: Optional[str] = None

    foto_perfil: Optional[str] = None           # Ruta relativa: fotos/personal_1_1700000000.png
    cv_archivo: Optional[str] = None            # Ruta relativa: cv/personal_1_1700000000.pdf
    documentos_extra: List[str] = []            # Lista de rutas relativas

    fecha_ingreso: Optional[str] = None
    estado_laboral: Optional[str] = None
    total_pacientes: Optional[int] = None
    sesiones_semana: Optional[int] = None
    rating: Optional[float] = None

    class Config:
        from_attributes = True

    @staticmethod
    def from_db(personal: Personal, perfil: PersonalPerfil, user: Usuario):
        # Parsear documentos_extra de JSON si existe
        docs_extra = []
        if perfil.documentos_extra:
            try:
                docs_extra = json.loads(perfil.documentos_extra)
            except (json.JSONDecodeError, TypeError):
                docs_extra = []

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

            foto_perfil=perfil.foto_perfil,
            cv_archivo=perfil.cv_archivo,
            documentos_extra=docs_extra,

            fecha_ingreso=str(personal.fecha_ingreso) if personal.fecha_ingreso else None,
            estado_laboral=str(personal.estado_laboral.value) if personal.estado_laboral else None,
            total_pacientes=personal.total_pacientes,
            sesiones_semana=personal.sesiones_semana,
            rating=personal.rating,
        )
