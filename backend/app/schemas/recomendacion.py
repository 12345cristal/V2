# app/schemas/recomendacion.py

from pydantic import BaseModel
from typing import Optional


class RecursoRecomendado(BaseModel):
    id: int
    titulo: str
    descripcion: str
    nivel_id: str
    categoria_id: str
    tipo_id: str
    etiquetas: list[str]
    score: float  # similitud

    class Config:
        from_attributes = True
