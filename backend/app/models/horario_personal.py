# app/models/horario_personal.py
from sqlalchemy import Column, Integer, Time, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class HorarioPersonal(Base):
    __tablename__ = "horarios_personal"

    id_horario = Column(Integer, primary_key=True, index=True)
    id_personal = Column(Integer, ForeignKey("personal.id_personal"), nullable=False)
    dia_semana = Column(SmallInteger, nullable=False)  # 1-7
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    personal = relationship("Personal", back_populates="horarios")
