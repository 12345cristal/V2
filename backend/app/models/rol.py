from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Rol(Base):
    """
    Roles del sistema (Administrador, Coordinador, Terapeuta, Padre)
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))

    # =========================
    # RELACIONES
    # =========================

    usuarios = relationship(
        "Usuario",
        back_populates="rol"
    )

    personal = relationship(
        "Personal",
        back_populates="rol"
    )

    # 🔥 ESTA RELACIÓN FALTABA
    permisos = relationship(
        "Permiso",
        secondary="roles_permisos",
        back_populates="roles"
    )

    def __repr__(self) -> str:
        return f"<Rol {self.nombre}>"
