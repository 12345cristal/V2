# backend/app/models/personal_perfil.py
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class PersonalPerfil(Base):
    """
    Tabla para información extendida del perfil de personal
    Contiene datos editables por el usuario
    """
    __tablename__ = "personal_perfil"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    personal_id = Column(Integer, ForeignKey("personal.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # Datos personales
    fecha_nacimiento = Column(Date, nullable=True)
    rfc = Column(String(13), nullable=True)
    ine = Column(String(18), nullable=True)
    curp = Column(String(18), nullable=True)
    
    # Académico
    grado_academico_id = Column(SmallInteger, ForeignKey("grado_academico.id", ondelete="SET NULL"), nullable=True)
    especialidades = Column(Text, nullable=True)  # JSON o lista separada por comas
    experiencia = Column(Text, nullable=True)
    
    # Contacto
    telefono_personal = Column(String(20), nullable=True)
    correo_personal = Column(String(100), nullable=True)
    
    # Domicilio
    domicilio_calle = Column(String(100), nullable=True)
    domicilio_colonia = Column(String(100), nullable=True)
    domicilio_cp = Column(String(10), nullable=True)
    domicilio_municipio = Column(String(100), nullable=True)
    domicilio_estado = Column(String(100), nullable=True)
    
    # Archivos
    cv_url = Column(String(255), nullable=True)
    foto_url = Column(String(255), nullable=True)
    
    # Relaciones
    personal = relationship("Personal", back_populates="perfil")
    grado_academico = relationship("GradoAcademico", foreign_keys=[grado_academico_id])
