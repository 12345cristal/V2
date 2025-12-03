# app/db/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos."""
    pass


# IMPORTANTE: importa los modelos para que Alembic los detecte
from app.models.rol import Rol  # noqa: F401
from app.models.permiso import Permiso, RolPermiso  # noqa: F401
from app.models.usuario import Usuario  # noqa: F401
from app.models.perfil_personal import PerfilPersonal  # noqa: F401
from app.models.nino import Nino  # noqa: F401
from app.models.notificacion import Notificacion  # noqa: F401
from app.models.decision_log import DecisionLog  # noqa: F401
from app.models.personal import Personal  # noqa: F401
from app.models.catalogos import (  # 👈 NUEVO
    CatGradoAcademico,
    CatEstadoLaboral,
    CatTipoTerapia,
    CatPrioridad,
    CatEstadoCita,
    CatNivelDificultad,
    CatTipoRecurso,
    CatCategoriaRecurso,
    CatNivelRecurso,
)  # noqa: F401
from app.models.terapia import Terapia  # si ya lo tienes
from app.models.personal_terapia import PersonalTerapia  # si ya lo tienes
from app.models.cita import Cita, CitaObservador  # lo creamos abajo
