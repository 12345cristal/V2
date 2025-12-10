# app/schemas/topsis.py
from pydantic import BaseModel, Field
from typing import List, Literal


# ============================================================
# SCHEMAS PARA CRITERIOS TOPSIS
# ============================================================

class CriterioTopsisBase(BaseModel):
    """Base schema para CriterioTopsis"""
    nombre: str = Field(..., max_length=100, description="Nombre del criterio")
    descripcion: str | None = Field(None, max_length=255, description="Descripción del criterio")
    peso: float = Field(..., ge=0.0, le=1.0, description="Peso del criterio (0-1)")
    tipo: Literal["beneficio", "costo"] = Field(..., description="Tipo de criterio: beneficio o costo")
    activo: int = Field(1, description="Estado del criterio")


class CriterioTopsisCreate(CriterioTopsisBase):
    """Schema para crear un criterio TOPSIS"""
    pass


class CriterioTopsisUpdate(BaseModel):
    """Schema para actualizar un criterio TOPSIS"""
    nombre: str | None = Field(None, max_length=100)
    descripcion: str | None = Field(None, max_length=255)
    peso: float | None = Field(None, ge=0.0, le=1.0)
    tipo: Literal["beneficio", "costo"] | None = None
    activo: int | None = None


class CriterioTopsisRead(CriterioTopsisBase):
    """Schema para leer un criterio TOPSIS"""
    id: int

    class Config:
        from_attributes = True


# ============================================================
# SCHEMAS PARA CÁLCULO TOPSIS
# ============================================================

class TopsisInput(BaseModel):
    """
    Input para el cálculo TOPSIS
    ids: lista de IDs de niños a evaluar
    matriz: matriz de decisión donde cada fila es un niño y cada columna un criterio
    """
    ids: List[int] = Field(..., description="Lista de IDs de niños a priorizar")
    matriz: List[List[float]] = Field(..., description="Matriz de decisión (filas=niños, columnas=criterios)")


class TopsisResultado(BaseModel):
    """
    Resultado del cálculo TOPSIS
    """
    nino_id: int = Field(..., description="ID del niño")
    score: float = Field(..., description="Score TOPSIS calculado (0-1)")
    ranking: int = Field(..., description="Posición en el ranking (1=mejor)")
    
    class Config:
        from_attributes = True
