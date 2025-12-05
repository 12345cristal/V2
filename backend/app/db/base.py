
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:  # se ignora si la clase define __tablename__
        return cls.__name__.lower()


# IMPORTA TODOS LOS MODELOS AQUÍ
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.models.rol_permiso import RolPermiso
from app.models.usuario import Usuario
from app.models.auditoria import Auditoria

from app.models.catalogos import (
    CatGradoAcademico,
    CatEstadoLaboral,
    CatTipoTerapia,
    CatPrioridad,
    CatEstadoCita,
    CatNivelDificultad,
    CatTipoRecurso,
    CatCategoriaRecurso,
    CatNivelRecurso,
)
from app.models.perfiles_personal import PerfilPersonal
from app.models.personal import Personal
from app.models.tutores import Tutor, TutorDireccion
from app.models.ninos import (
    Nino,
    NinoDireccion,
    NinoDiagnostico,
    NinoAlergias,
    NinoMedicamentosActuales,
    NinoEscolar,
    NinoContactoEmergencia,
    NinoInfoEmocional,
    NinoArchivos,
)
from app.models.terapias import (
    Terapia,
    PersonalTerapia,
    TerapiaNino,
    SesionTerapia,
    ReposicionTerapia,
)
from app.models.citas import Cita, CitaObservador
from app.models.actividades_recursos import (
    Actividad,
    RecomendacionActividad,
    RecursoTerapeuta,
    RecursoTarea,
    ValoracionActividad,
)
from app.models.notificaciones import Notificacion
from app.models.decision_logs import DecisionLog
