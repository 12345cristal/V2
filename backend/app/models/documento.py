# app/models/documento.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
import enum


class TipoDocumento(str, enum.Enum):
    ACUERDO_SERVICIOS = "ACUERDO_SERVICIOS"
    REPORTE_TERAPEUTICO = "REPORTE_TERAPEUTICO"
    DOCUMENTO_MEDICO = "DOCUMENTO_MEDICO"
    ACTUALIZACION_MEDICAMENTOS = "ACTUALIZACION_MEDICAMENTOS"
    OTRO = "OTRO"


class Documento(Base):
    """Modelo de Documentos para niños"""
    __tablename__ = "documentos"
    
    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo_documento = Column(Enum(TipoDocumento), nullable=False)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    url_archivo = Column(String(500), nullable=False)
    tipo_archivo = Column(String(50), default="application/pdf")
    tamanio_bytes = Column(Integer, nullable=True)
    nuevo = Column(Boolean, default=True)
    activo = Column(Boolean, default=True, index=True)
    subido_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_subida = Column(DateTime, default=datetime.utcnow, index=True)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    nino = relationship("Nino", back_populates="documentos")
    usuario = relationship("Usuario")
    vistos = relationship("DocumentoVisto", back_populates="documento", cascade="all, delete-orphan")


class DocumentoVisto(Base):
    """Registro de documentos vistos por usuarios"""
    __tablename__ = "documentos_vistos"
    
    id = Column(Integer, primary_key=True, index=True)
    documento_id = Column(Integer, ForeignKey("documentos.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    visto = Column(Boolean, default=True)
    fecha_visto = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    documento = relationship("Documento", back_populates="vistos")
    usuario = relationship("Usuario")
    
    __table_args__ = (
        {'sqlite_autoincrement': True},
    )