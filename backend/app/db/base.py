# app/db/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# IMPORTA AQUÍ TODOS LOS MODELOS PARA QUE ALEMBIC LOS VEA
from app.models import role, permiso, usuario, personal, tutor, nino  # noqa
