from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, SmallInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(60), nullable=False)
    apellido_materno = Column(String(60))
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    telefono = Column(String(20))
    activo = Column(SmallInteger, nullable=False, default=1)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    ultimo_login = Column(DateTime)

    # Relationships
    rol = relationship("Rol", back_populates="usuarios")
    personal = relationship("Personal", back_populates="usuario", uselist=False)
    tutor = relationship("Tutor", back_populates="usuario", uselist=False)
    notificaciones = relationship("Notificacion", back_populates="usuario")
    decision_logs = relationship("DecisionLog", back_populates="usuario")
    auditorias = relationship("Auditoria", back_populates="usuario")
