# app/models/__init__.py
"""
Modelos SQLAlchemy para Autismo Mochis IA
Importar todos los modelos aquí para que SQLAlchemy los registre
"""

from app.db.base_class import Base

# Catálogos
from app.models.catalogos import (
    GradoAcademico,
    EstadoLaboral,
    TipoTerapia,
    Prioridad,
    EstadoCita,
    NivelDificultad,
    TipoRecurso,
    CategoriaRecurso,
    NivelRecurso
)

# Usuarios y autenticación
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.models.role_permiso import RolePermiso

# Personal
from app.models.personal import Personal, PersonalPerfil, PersonalHorario

# Tutores
from app.models.tutor import Tutor, TutorDireccion

# Niños
from app.models.nino import (
    Nino,
    NinoDireccion,
    NinoDiagnostico,
    NinoInfoEmocional,
    NinoArchivos
)

# Terapias
from app.models.terapia import (
    Terapia,
    TerapiaPersonal,
    TerapiaNino,
    Sesion,
    Reposicion
)

# Citas
from app.models.cita import Cita

# Recursos y tareas
from app.models.recurso import (
    Recurso,
    TareaRecurso,
    Valoracion,
    Recomendacion
)

# Sistema
from app.models.notificacion import Notificacion
from app.models.decision_log import DecisionLog
from app.models.auditoria import Auditoria

__all__ = [
    "Base",
    # Catálogos
    "GradoAcademico", "EstadoLaboral", "TipoTerapia", "Prioridad",
    "EstadoCita", "NivelDificultad", "TipoRecurso", "CategoriaRecurso", "NivelRecurso",
    # Auth
    "Usuario", "Rol", "Permiso", "RolePermiso",
    # Personal
    "Personal", "PersonalPerfil", "PersonalHorario",
    # Tutores
    "Tutor", "TutorDireccion",
    # Niños
    "Nino", "NinoDireccion", "NinoDiagnostico", "NinoInfoEmocional", "NinoArchivos",
    # Terapias
    "Terapia", "TerapiaPersonal", "TerapiaNino", "Sesion", "Reposicion",
    # Citas
    "Cita",
    # Recursos
    "Recurso", "TareaRecurso", "Valoracion", "Recomendacion",
    # Sistema
    "Notificacion", "DecisionLog", "Auditoria"
]
