# app/models/bitacora.py (ejemplo mínimo, adáptalo a tu modelo real)

from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Bitacora(Base):
    __tablename__ = "bitacoras"

    id_bitacora = Column(Integer, primary_key=True, index=True)
    id_sesion = Column(Integer, index=True)
    id_nino = Column(Integer, index=True)
    texto = Column(Text, nullable=False)
    creado_en = Column(DateTime, server_default=func.now())
