# app/db/base_class.py
from typing import Any
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr


class Base(DeclarativeBase):
    """Clase base para todos los modelos SQLAlchemy"""

    id: Any
    __name__: str

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
