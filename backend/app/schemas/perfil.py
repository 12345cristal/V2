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

    foto_perfil: Optional[str] = None
    cv_archivo: Optional[str] = None
    documentos_extra: Optional[List[str]] = None

    fecha_ingreso: Optional[str] = None
    estado_laboral: Optional[str] = None
    total_pacientes: Optional[int] = None
    sesiones_semana: Optional[int] = None
    rating: Optional[float] = None

    class Config:
        from_attributes = True

    def to_json(self):
        return {
            "id_personal": self.id_personal,
            "nombres": self.nombres,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "fecha_nacimiento": self.fecha_nacimiento,
            "telefono_personal": self.telefono_personal,
            "correo_personal": self.correo_personal,
            "grado_academico": self.grado_academico,
            "especialidad_principal": self.especialidad_principal,
            "especialidades": self.especialidades,
            "experiencia": self.experiencia,
            "domicilio_calle": self.domicilio_calle,
            "domicilio_colonia": self.domicilio_colonia,
            "domicilio_cp": self.domicilio_cp,
            "domicilio_municipio": self.domicilio_municipio,
            "domicilio_estado": self.domicilio_estado,
            "fecha_ingreso": self.fecha_ingreso,
            "estado_laboral": self.estado_laboral,
            "total_pacientes": self.total_pacientes,
            "sesiones_semana": self.sesiones_semana,
            "rating": self.rating,
            "foto_perfil": self.foto_perfil,
            "cv_archivo": self.cv_archivo,
            "documentos_extra": self.documentos_extra,
        }

    @staticmethod
    def from_db(personal: Personal, perfil: PersonalPerfil, user: Usuario):
        # Parse documentos_extra if it's JSON
        documentos = None
        if perfil.documentos_extra:
            try:
                documentos = json.loads(perfil.documentos_extra)
            except:
                documentos = []
        
        return PerfilResponse(
            id_personal=personal.id,

            nombres=personal.nombres,
            apellido_paterno=personal.apellido_paterno,
            apellido_materno=personal.apellido_materno,

            fecha_nacimiento=str(personal.fecha_nacimiento) if personal.fecha_nacimiento else None,

            telefono_personal=perfil.telefono_personal or personal.telefono_personal,
            correo_personal=perfil.correo_personal or personal.correo_personal,

            grado_academico=perfil.grado_academico,
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
            documentos_extra=documentos,

            fecha_ingreso=str(personal.fecha_ingreso) if personal.fecha_ingreso else None,
            estado_laboral=str(personal.estado_laboral.value) if personal.estado_laboral else None,
            total_pacientes=personal.total_pacientes,
            sesiones_semana=personal.sesiones_semana,
            rating=personal.rating,
        )

