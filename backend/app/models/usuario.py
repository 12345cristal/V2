# app/models/usuario.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Usuario(Base):
    """Modelo de Usuarios"""
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(60), nullable=False)
    apellido_materno = Column(String(60))
    email = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    telefono = Column(String(20))
    activo = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    ultimo_login = Column(DateTime)
    
    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    personal = relationship("Personal", back_populates="usuario")
    notificaciones = relationship("Notificacion", back_populates="usuario", cascade="all, delete-orphan")
    tareas_creadas = relationship("Tarea", foreign_keys="Tarea.terapeuta_id", back_populates="terapeuta")
