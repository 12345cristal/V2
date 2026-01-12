from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)  # padre, terapeuta, admin
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.now)
    ultimo_acceso = Column(DateTime)
    
    # Relaciones
    padre = relationship("Padre", back_populates="usuario", uselist=False)
    terapeuta = relationship("Terapeuta", back_populates="usuario", uselist=False)


class Padre(Base):
    __tablename__ = "padres"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    telefono = Column(String(20))
    direccion = Column(String(500))
    ocupacion = Column(String(255))
    
    usuario = relationship("Usuario", back_populates="padre")
    hijos = relationship("Hijo", back_populates="padre")


class Terapeuta(Base):
    __tablename__ = "terapeutas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    especialidad = Column(String(255))
    cedula_profesional = Column(String(100))
    telefono = Column(String(20))
    anos_experiencia = Column(Integer)
    biografia = Column(Text)
    
    usuario = relationship("Usuario", back_populates="terapeuta")
    recursos = relationship("Recurso", back_populates="terapeuta")
    asignaciones = relationship("AsignacionTerapeuta", back_populates="terapeuta")
    sesiones = relationship("Sesion", back_populates="terapeuta")


class Hijo(Base):
    __tablename__ = "hijos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    diagnostico = Column(String(255))
    nivel_tea = Column(String(50))  # Leve, Moderado, Severo
    observaciones = Column(Text)
    foto_perfil = Column(String(500))
    padre_id = Column(Integer, ForeignKey("usuarios.id"))
    
    padre = relationship("Padre", back_populates="hijos")
    asignaciones = relationship("AsignacionTerapeuta", back_populates="hijo")
    sesiones = relationship("Sesion", back_populates="hijo")
    progresos = relationship("Progreso", back_populates="hijo")


class AsignacionTerapeuta(Base):
    __tablename__ = "asignaciones_terapeuta"
    
    id = Column(Integer, primary_key=True, index=True)
    terapeuta_id = Column(Integer, ForeignKey("terapeutas.id"))
    hijo_id = Column(Integer, ForeignKey("hijos.id"))
    fecha_asignacion = Column(DateTime, default=datetime.now)
    fecha_fin = Column(DateTime)
    activo = Column(Boolean, default=True)
    
    terapeuta = relationship("Terapeuta", back_populates="asignaciones")
    hijo = relationship("Hijo", back_populates="asignaciones")


class Sesion(Base):
    __tablename__ = "sesiones"
    
    id = Column(Integer, primary_key=True, index=True)
    terapeuta_id = Column(Integer, ForeignKey("terapeutas.id"))
    hijo_id = Column(Integer, ForeignKey("hijos.id"))
    fecha = Column(DateTime, nullable=False)
    duracion = Column(Integer)  # en minutos
    tipo = Column(String(100))  # individual, grupal, evaluacion
    estado = Column(String(50), default="programada")  # programada, completada, cancelada
    objetivo = Column(Text)
    notas = Column(Text)
    materiales = Column(Text)
    
    terapeuta = relationship("Terapeuta", back_populates="sesiones")
    hijo = relationship("Hijo", back_populates="sesiones")


class Progreso(Base):
    __tablename__ = "progresos"
    
    id = Column(Integer, primary_key=True, index=True)
    hijo_id = Column(Integer, ForeignKey("hijos.id"))
    fecha = Column(DateTime, default=datetime.now)
    area = Column(String(100))  # comunicacion, social, conducta, sensorial, cognitivo
    nivel = Column(String(50))  # En desarrollo, Logrado, Requiere apoyo
    puntuacion = Column(Float)
    observaciones = Column(Text)
    evaluador = Column(String(255))
    
    hijo = relationship("Hijo", back_populates="progresos")


class Recurso(Base):
    __tablename__ = "recursos"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)
    tipo_recurso = Column(String(50), nullable=False)  # PDF, VIDEO, ENLACE
    categoria_recurso = Column(String(100))
    nivel_recurso = Column(String(50))
    url = Column(String(500))
    archivo = Column(String(500))
    objetivo_terapeutico = Column(Text)
    terapeuta_id = Column(Integer, ForeignKey("terapeutas.id"))
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    terapeuta = relationship("Terapeuta", back_populates="recursos")
    recomendaciones = relationship("Recomendacion", back_populates="recurso")


class Recomendacion(Base):
    __tablename__ = "recomendaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    recurso_id = Column(Integer, ForeignKey("recursos.id"))
    hijo_id = Column(Integer, ForeignKey("hijos.id"))
    terapeuta_id = Column(Integer, ForeignKey("terapeutas.id"))
    fecha_recomendacion = Column(DateTime, default=datetime.now)
    notas_terapeuta = Column(Text)
    
    recurso = relationship("Recurso", back_populates="recomendaciones")


class RecursoVisto(Base):
    __tablename__ = "recursos_vistos"
    
    id = Column(Integer, primary_key=True, index=True)
    recurso_id = Column(Integer, ForeignKey("recursos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_visto = Column(DateTime, default=datetime.now)
    
    __table_args__ = (
        UniqueConstraint('recurso_id', 'usuario_id', name='uq_recurso_usuario'),
    )
    