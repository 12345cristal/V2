# app/models/__init__.py
<<<<<<< HEAD

# =========================
# Seguridad y roles
=======
# =========================
# SEGURIDAD Y USUARIOS
>>>>>>> 85852a6 (uno que otro movimiento para loguearme y de rutas)
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
<<<<<<< HEAD
=======

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
>>>>>>> 85852a6 (uno que otro movimiento para loguearme y de rutas)
from app.models.personal import Personal, PersonalHorario
from app.models.personal_perfil import PersonalPerfil
from app.models.grado_academico import GradoAcademico

# =========================
<<<<<<< HEAD
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
=======
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
>>>>>>> 85852a6 (uno que otro movimiento para loguearme y de rutas)
# =========================
from app.models.tarea_recurso import TareaRecurso

# =========================
# Pagos
# =========================
from app.models.plan_pago import PlanPago
from app.models.pago import Pago

# =========================
<<<<<<< HEAD
# Otros
# =========================
=======
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
>>>>>>> 85852a6 (uno que otro movimiento para loguearme y de rutas)
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
<<<<<<< HEAD
    "Personal",
    "PersonalHorario",
    "PersonalPerfil",
    "GradoAcademico",
=======
>>>>>>> 85852a6 (uno que otro movimiento para loguearme y de rutas)

    # Niños
    "Nino",
    "NinoDireccion",
    "NinoDiagnostico",
    "NinoInfoEmocional",
    "NinoArchivos",

<<<<<<< HEAD
=======
    # Personal
    "Personal",
    "PersonalHorario",
    "PersonalPerfil",
    "GradoAcademico",

>>>>>>> 85852a6 (uno que otro movimiento para loguearme y de rutas)
    # Terapias
    "Terapia",
    "TerapiaPersonal",
    "TerapiaNino",
    "TipoTerapia",
    "Prioridad",
    "Sesion",
    "Reposicion",
<<<<<<< HEAD
=======
    "Progreso",
>>>>>>> 85852a6 (uno que otro movimiento para loguearme y de rutas)

    # Recursos
    "Recurso",
    "Recomendacion",
    "RecursoVisto",
<<<<<<< HEAD

    # Tareas
=======
    "TipoRecurso",
    "CategoriaRecurso",
    "NivelRecurso",

    # Tareas / Pagos
>>>>>>> 85852a6 (uno que otro movimiento para loguearme y de rutas)
    "TareaRecurso",

    # Pagos
    "PlanPago",
    "Pago",

<<<<<<< HEAD
    # Otros
    "Notificacion",
    "Documento",
    "DocumentoVisto",
    "Paciente",
=======
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
>>>>>>> 85852a6 (uno que otro movimiento para loguearme y de rutas)
]
