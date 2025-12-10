# app/models/criterio_topsis.py
from sqlalchemy import Column, Integer, String, DECIMAL, Enum
from app.db.base_class import Base


class CriterioTopsis(Base):
    """
    Modelo para criterios de evaluación TOPSIS
    Permite configurar los criterios que se usarán para priorizar niños
    """
    __tablename__ = "criterio_topsis"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255))
    peso = Column(DECIMAL(5, 4), nullable=False, default=1.0)
    tipo = Column(
        Enum("beneficio", "costo", name="tipo_criterio_enum"),
        nullable=False,
        default="beneficio"
    )
    activo = Column(Integer, default=1)

    def __repr__(self):
        return f"<CriterioTopsis(id={self.id}, nombre='{self.nombre}', peso={self.peso}, tipo='{self.tipo}')>"
