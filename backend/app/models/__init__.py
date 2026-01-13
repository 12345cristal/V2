# app/models/__init__.py

# =========================
# Seguridad y roles
# =========================
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.models.role_permiso import RolePermiso

# =========================
# Usuarios y perfiles
# =========================
from app.models.usuario import Usuario
from app.models.tutor import Tutor, TutorDireccion
from app.models.personal import Personal, PersonalHorario
from app.models.personal_perfil import PersonalPerfil
from app.models.grado_academico import GradoAcademico

# =========================
# Niños
# =========================
from app.models.nino import (
    Nino,
    NinoDireccion,
    NinoDiagnostico,
    NinoInfoEmocional,
    NinoArchivos,
)

# =========================
# Terapias y sesiones
# =========================
from app.models.terapia import (
    Terapia,
    TerapiaPersonal,
    TerapiaNino,
    TipoTerapia,
    Prioridad,
    Sesion,
    Reposicion,
)

# =========================
# Recursos y recomendaciones
# =========================
from app.models.recurso import Recurso
from app.models.recomendacion import RecomendacionActividad as Recomendacion1
from app.models.recurso_visto import RecursoVisto
from app.models.recomendacion import PerfilNinoVectorizado, PerfilActividadVectorizada, HistorialProgreso, AsignacionTerapeutaTOPSIS
# =========================
# Tareas
# =========================
from app.models.tarea_recurso import TareaRecurso

# =========================
# Pagos
# =========================
from app.models.plan_pago import PlanPago
from app.models.pago import Pago

# =========================
# Otros
# =========================
from app.models.notificacion import Notificacion
from app.models.documento import Documento, DocumentoVisto
from app.models.paciente import Paciente


__all__ = [
    # Seguridad
    "Rol",
    "Permiso",
    "RolePermiso",

    # Usuarios
    "Usuario",
    "Tutor",
    "TutorDireccion",
    "Personal",
    "PersonalHorario",
    "PersonalPerfil",
    "GradoAcademico",

    # Niños
    "Nino",
    "NinoDireccion",
    "NinoDiagnostico",
    "NinoInfoEmocional",
    "NinoArchivos",

    # Terapias
    "Terapia",
    "TerapiaPersonal",
    "TerapiaNino",
    "TipoTerapia",
    "Prioridad",
    "Sesion",
    "Reposicion",

    # Recursos
    "Recurso",
    "Recomendacion",
    "RecursoVisto",

    # Tareas
    "TareaRecurso",

    # Pagos
    "PlanPago",
    "Pago",

    # Otros
    "Notificacion",
    "Documento",
    "DocumentoVisto",
    "Paciente",
]
