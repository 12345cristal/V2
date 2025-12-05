# app/models/nino.py
from sqlalchemy import Column, Integer, String, Date, Enum, Text
from app.db.session import Base


class EstadoNinoEnum(str, Enum):
    ACTIVO = "ACTIVO"
    EN_ESPERA = "EN_ESPERA"
    BAJA = "BAJA"


class Nino(Base):
    __tablename__ = "ninos"

    id_nino = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    fecha_nacimiento = Column(Date, nullable=False)
    diagnostico_principal = Column(Text, nullable=True)
    estado = Column(Enum(EstadoNinoEnum), default=EstadoNinoEnum.ACTIVO)

    # añade FK a tutor, escuela, etc. según tu BD
