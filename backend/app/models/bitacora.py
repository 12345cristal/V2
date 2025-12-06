from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Bitacora(Base):
    __tablename__ = "bitacoras"

    id_bitacora = Column(Integer, primary_key=True)
    id_sesion = Column(Integer, nullable=False)
    id_nino = Column(Integer, ForeignKey("ninos.id_nino"), nullable=False)
    id_terapeuta = Column(Integer, ForeignKey("personal.id_personal"), nullable=False)

    texto = Column(Text, nullable=False)
    creado_en = Column(DateTime, server_default=func.now())

    nino = relationship("Nino", backref="bitacoras")
    terapeuta = relationship("Personal")
