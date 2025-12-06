from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class Tutor(Base):
    __tablename__ = "tutores"

    id_tutor = Column(Integer, primary_key=True)
    nombre_completo = Column(String(150), nullable=False)
    correo = Column(String(150), nullable=False)
    telefono = Column(String(50))
