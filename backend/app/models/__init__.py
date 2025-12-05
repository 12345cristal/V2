# app/models/__init__.py
from app.db.base_class import Base  # noqa

from app.models.usuario import Usuario  # noqa
from app.models.rol import Rol  # noqa
from app.models.permiso import Permiso  # noqa
from app.models.rol_permiso import RolPermiso  # noqa

# aquí luego agregas más modelos (Nino, Terapia, etc.)
