# app/db/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos."""
    pass


# IMPORTANTE: importa los modelos para que Alembic los detecte
from app.models import role  # noqa: F401
from app.models import permiso  # noqa: F401
from app.models import usuario  # noqa: F401
from app.models import personal  # noqa: F401
from app.models import tutor  # noqa: F401
from app.models import nino  # noqa: F401
from app.models import notificacion  # noqa: F401
from app.models import decision_log  # noqa: F401
