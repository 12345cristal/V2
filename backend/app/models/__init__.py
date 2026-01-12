# app/models/__init__.py
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.models.role_permiso import RolePermiso
from app.models.usuario import Usuario
from app.models.tutor import Tutor, TutorDireccion
from app.models.nino import Nino, NinoDireccion, NinoDiagnostico, NinoInfoEmocional, NinoArchivos
from app.models.medicamentos import Medicamento, Alergia
from app.models.personal import Personal, PersonalHorario
from app.models.personal_perfil import PersonalPerfil
from app.models.grado_academico import GradoAcademico
from app.models.terapia import (
    Terapia, 
    TerapiaPersonal, 
    TerapiaNino, 
    TipoTerapia, 
    Prioridad, 
    Sesion, 
    Reposicion
)
from app.models.cita import Cita, EstadoCita
from app.models.chat import ChatSession, ChatMessage
from app.models.ficha_emergencia import FichaEmergencia
from app.models.criterio_topsis import CriterioTopsis
from app.models.actividad import Actividad
from app.models.recomendacion import (
    PerfilNinoVectorizado,
    PerfilActividadVectorizada,
    HistorialProgreso,
    RecomendacionActividad,
    AsignacionTerapeutaTOPSIS
)

__all__ = [
    "Rol",
    "Permiso",
    "RolePermiso",
    "Usuario",
    "Tutor",
    "TutorDireccion",
    "Nino",
    "NinoDireccion",
    "NinoDiagnostico",
    "NinoInfoEmocional",
    "NinoArchivos",
    "Medicamento",
    "Alergia",
    "Personal",
    "PersonalHorario",
    "PersonalPerfil",
    "GradoAcademico",
    "Terapia",
    "TerapiaPersonal",
    "TerapiaNino",
    "TipoTerapia",
    "Prioridad",
    "Sesion",
    "Reposicion",
    "Cita",
    "EstadoCita",
    "ChatSession",
    "ChatMessage",
    "FichaEmergencia",
    "CriterioTopsis",
    "Actividad",
    "PerfilNinoVectorizado",
    "PerfilActividadVectorizada",
    "HistorialProgreso",
    "RecomendacionActividad",
    "AsignacionTerapeutaTOPSIS"
]
