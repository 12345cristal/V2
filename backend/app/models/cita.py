# app/models/cita.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Time, SmallInteger, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class EstadoCita(Base):
    """
    Catálogo de estados de citas
    """
    __tablename__ = "estado_cita"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class Cita(Base):
    """
    Modelo para la tabla 'citas'
    Representa las citas programadas entre niños y terapeutas
    
    EXTENSIÓN: Incluye integración con Google Calendar
    """
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="SET NULL"))
    terapeuta_id = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))
    terapia_id = Column(Integer, ForeignKey("terapias.id", ondelete="SET NULL"))
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado_id = Column(SmallInteger, ForeignKey("estado_cita.id"), nullable=False)
    motivo = Column(Text)
    observaciones = Column(Text)
    es_reposicion = Column(SmallInteger, default=0)
    
    # === NUEVOS CAMPOS: Integración Google Calendar ===
    google_event_id = Column(String(255), nullable=True, unique=True, index=True, 
                            comment="ID del evento en Google Calendar")
    google_calendar_link = Column(String(500), nullable=True, 
                                  comment="URL del evento en Google Calendar")
    sincronizado_calendar = Column(Boolean, default=False, 
                                   comment="Indica si está sincronizado con Google Calendar")
    fecha_sincronizacion = Column(DateTime, nullable=True, 
                                  comment="Última fecha de sincronización con Google Calendar")
    
    # === CAMPOS ADICIONALES DE GESTIÓN ===
    confirmada = Column(Boolean, default=False, comment="Confirmada por el padre/tutor")
    fecha_confirmacion = Column(DateTime, nullable=True)
    cancelado_por = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    fecha_cancelacion = Column(DateTime, nullable=True)
    motivo_cancelacion = Column(Text, nullable=True)
    
    # Auditoría
    creado_por = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    actualizado_por = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    nino = relationship("Nino", foreign_keys=[nino_id])
    terapeuta = relationship("Personal", foreign_keys=[terapeuta_id])
    terapia = relationship("Terapia", foreign_keys=[terapia_id])
    estado = relationship("EstadoCita", foreign_keys=[estado_id])
    usuario_creador = relationship("Usuario", foreign_keys=[creado_por])
    usuario_actualizador = relationship("Usuario", foreign_keys=[actualizado_por])
    usuario_cancelador = relationship("Usuario", foreign_keys=[cancelado_por])
