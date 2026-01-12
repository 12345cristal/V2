from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Conversacion(Base):
    __tablename__ = "conversaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("hijos.id"), nullable=True)
    creada_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(String(40), default="CHAT_GENERAL")
    activa = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    participantes = relationship("ConversacionParticipante", back_populates="conversacion")
    mensajes = relationship("Mensaje", back_populates="conversacion")
    creador = relationship("Usuario")


class ConversacionParticipante(Base):
    __tablename__ = "conversacion_participantes"
    
    id = Column(Integer, primary_key=True, index=True)
    conversacion_id = Column(Integer, ForeignKey("conversaciones.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.now)
    last_seen_at = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True)
    
    conversacion = relationship("Conversacion", back_populates="participantes")
    usuario = relationship("Usuario")
    
    __table_args__ = (
        UniqueConstraint('conversacion_id', 'usuario_id', name='uq_conv_usuario'),
    )


class Mensaje(Base):
    __tablename__ = "mensajes"
    
    id = Column(Integer, primary_key=True, index=True)
    conversacion_id = Column(Integer, ForeignKey("conversaciones.id"), nullable=False)
    emisor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(String(20), default="TEXTO")  # TEXTO, AUDIO, ARCHIVO
    contenido = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    eliminado = Column(Boolean, default=False)
    
    conversacion = relationship("Conversacion", back_populates="mensajes")
    emisor = relationship("Usuario")
    archivos = relationship("MensajeArchivo", back_populates="mensaje")
    vistos = relationship("MensajeVisto", back_populates="mensaje")


class MensajeArchivo(Base):
    __tablename__ = "mensajes_archivos"
    
    id = Column(Integer, primary_key=True, index=True)
    mensaje_id = Column(Integer, ForeignKey("mensajes.id"), nullable=False)
    archivo_url = Column(String(500), nullable=False)
    tipo_archivo = Column(String(50))
    nombre_original = Column(String(255))
    tamanio_bytes = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    
    mensaje = relationship("Mensaje", back_populates="archivos")


class MensajeVisto(Base):
    __tablename__ = "mensajes_vistos"
    
    id = Column(Integer, primary_key=True, index=True)
    mensaje_id = Column(Integer, ForeignKey("mensajes.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    visto = Column(Boolean, default=True)
    visto_at = Column(DateTime, default=datetime.now)
    
    mensaje = relationship("Mensaje", back_populates="vistos")
    usuario = relationship("Usuario")
    
    __table_args__ = (
        UniqueConstraint('mensaje_id', 'usuario_id', name='uq_msg_usuario'),
    )