from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Permiso(Base):
    """
    Modelo de permisos del sistema
    (ej: USUARIOS_VER, TERAPIAS_EDITAR, PAGOS_ADMIN)
    """
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(120), nullable=False, unique=True, index=True)
    descripcion = Column(String(150))

    # =========================
    # RELACIONES
    # =========================
    roles = relationship(
        "Rol",
        secondary="roles_permisos",
        back_populates="permisos"
    )

    def __repr__(self) -> str:
        return f"<Permiso {self.codigo}>"
