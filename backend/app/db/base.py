
# app/db/base.py  (cuando ya tengas todos los modelos)
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


# Importa aquí todos los modelos para que Alembic los vea
# from app.models.roles import Rol
# from app.models.usuarios import Usuario
# from app.models.auditoria import Auditoria
# ...
