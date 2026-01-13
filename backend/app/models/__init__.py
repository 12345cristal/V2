# app/models/__init__.py
# =========================
# SEGURIDAD Y USUARIOS
# =========================
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.models.role_permiso import RolePermiso

# =========================
# Usuarios y perfiles
# =========================
from app.models.usuario import Usuario

# =========================
# TUTORES / PADRES
# =========================
from app.models.tutor import Tutor, TutorDireccion

# =========================
# NIÑOS (TEA)
# =========================
from app.models.nino import (
    Nino,
    NinoDireccion,
    NinoDiagnostico,
    NinoInfoEmocional,
    NinoArchivos,
)

# =========================
# PERSONAL / TERAPEUTAS
# =========================
from app.models.personal import Personal, PersonalHorario
from app.models.personal_perfil import PersonalPerfil
from app.models.grado_academico import GradoAcademico

# =========================
# TERAPIAS Y SESIONES
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

from app.models.progreso import Progreso

# =========================
# RECURSOS TERAPÉUTICOS
# =========================
from app.models.recurso import (
    Recurso,
    Recomendacion,
    RecursoVisto,
    TipoRecurso,
    CategoriaRecurso,
    NivelRecurso,
)

# =========================
# TAREAS Y PAGOS
# =========================
from app.models.tarea_recurso import TareaRecurso

# =========================
# Pagos
# =========================
from app.models.plan_pago import PlanPago
from app.models.pago import Pago

# =========================
# IA / ANÁLISIS
# =========================
from app.models.criterio_topsis import CriterioTopsis
from app.models.actividad import Actividad
from app.models.recomendacion import (
    PerfilNinoVectorizado,
    PerfilActividadVectorizada,
    HistorialProgreso,
    RecomendacionActividad,
    AsignacionTerapeutaTOPSIS,
)

# =========================
# OTROS
# =========================
from app.models.paciente import Paciente
from app.models.notificacion import Notificacion
from app.models.documento import Documento, DocumentoVisto
from app.models.paciente import Paciente



# =========================
# EXPORTS OFICIALES
# =========================
__all__ = [
    # Seguridad
    "Rol",
    "Permiso",
    "RolePermiso",

    # Usuarios
    "Usuario",

    # Tutores
    "Tutor",
    "TutorDireccion",

    # Niños
    "Nino",
    "NinoDireccion",
    "NinoDiagnostico",
    "NinoInfoEmocional",
    "NinoArchivos",

    # Personal
    "Personal",
    "PersonalHorario",
    "PersonalPerfil",
    "GradoAcademico",

    # Terapias
    "Terapia",
    "TerapiaPersonal",
    "TerapiaNino",
    "TipoTerapia",
    "Prioridad",
    "Sesion",
    "Reposicion",
    "Progreso",

    # Recursos
    "Recurso",
    "Recomendacion",
    "RecursoVisto",
    "TipoRecurso",
    "CategoriaRecurso",
    "NivelRecurso",

    # Tareas / Pagos
    "TareaRecurso",

    # Pagos
    "PlanPago",
    "Pago",

    # IA / análisis
    "CriterioTopsis",
    "Actividad",
    "PerfilNinoVectorizado",
    "PerfilActividadVectorizada",
    "HistorialProgreso",
    "RecomendacionActividad",
    "AsignacionTerapeutaTOPSIS",

    # Otros
    "Paciente",
    "Notificacion",
]
