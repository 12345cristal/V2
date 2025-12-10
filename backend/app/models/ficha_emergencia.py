# app/models/ficha_emergencia.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class FichaEmergencia(Base):
    """
    Ficha de emergencia del niño
    Contiene información crítica para situaciones de emergencia
    """
    __tablename__ = "fichas_emergencia"

    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Información médica crítica
    tipo_sangre = Column(String(10))  # A+, B+, AB+, O+, A-, B-, AB-, O-
    alergias = Column(Text)  # Alergias conocidas (medicamentos, alimentos, etc.)
    condiciones_medicas = Column(Text)  # Condiciones médicas adicionales
    medicamentos_actuales = Column(Text)  # Medicamentos que toma actualmente
    
    # Información de diagnóstico
    diagnostico_principal = Column(String(255))
    diagnostico_detallado = Column(Text)
    
    # Contactos de emergencia (principal)
    contacto_principal_nombre = Column(String(200), nullable=False)
    contacto_principal_relacion = Column(String(100))  # Padre, Madre, Tutor, etc.
    contacto_principal_telefono = Column(String(20), nullable=False)
    contacto_principal_telefono_alt = Column(String(20))
    
    # Contacto de emergencia secundario
    contacto_secundario_nombre = Column(String(200))
    contacto_secundario_relacion = Column(String(100))
    contacto_secundario_telefono = Column(String(20))
    
    # Información médica adicional
    seguro_medico = Column(String(200))
    numero_seguro = Column(String(100))
    hospital_preferido = Column(String(255))
    medico_tratante = Column(String(200))
    telefono_medico = Column(String(20))
    
    # Instrucciones especiales
    instrucciones_emergencia = Column(Text)  # Qué hacer en caso de emergencia
    restricciones_alimenticias = Column(Text)
    
    # Información de comportamiento crítica
    crisis_comunes = Column(Text)  # Tipos de crisis que puede presentar
    como_calmar = Column(Text)  # Técnicas efectivas para calmarlo
    trigger_points = Column(Text)  # Situaciones que desencadenan crisis
    
    # Control
    activa = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creado_por_id = Column(Integer, ForeignKey("usuarios.id"))
    
    # Relaciones
    nino = relationship("Nino", backref="ficha_emergencia")
    creado_por = relationship("Usuario")
