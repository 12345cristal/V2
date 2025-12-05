from sqlalchemy.orm import declarative_base

Base = declarative_base()

# IMPORTA TODOS LOS MODELOS PARA QUE ALEMBIC LOS VEA
from app.models.catalogos import (  # noqa
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
from app.models.roles_usuarios import (  # noqa
    Rol,
    Permiso,
    RolPermiso,
    Usuario,
    PerfilPersonal,
    Personal,
)
from app.models.tutores import (  # noqa
    Tutor,
    TutorDireccion,
)
from app.models.ninos import (  # noqa
    Nino,
    NinoDireccion,
    NinoDiagnostico,
    NinoAlergias,
    NinoMedicamentoActual,
    NinoEscolar,
    NinoContactoEmergencia,
    NinoInfoEmocional,
    NinoArchivos,
)
from app.models.terapias import (  # noqa
    Terapia,
    PersonalTerapia,
    TerapiaNino,
    SesionTerapia,
    ReposicionTerapia,
)
from app.models.citas import (  # noqa
    Cita,
    CitaObservador,
)
from app.models.actividades import (  # noqa
    Actividad,
    RecomendacionActividad,
)
from app.models.recursos import (  # noqa
    RecursoTerapeuta,
    RecursoTarea,
    ValoracionActividad,
)
from app.models.notificaciones import Notificacion  # noqa
from app.models.ia import DecisionLog  # noqa
from app.models.auditoria import Auditoria  # noqa
