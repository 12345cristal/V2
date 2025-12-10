# backend/app/schemas/topsis_terapeutas.py
"""
Schemas Pydantic para el módulo TOPSIS de Selección de Terapeutas
Implementa validaciones robustas y tipos estrictos
"""
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Dict
from decimal import Decimal


class PesosCriterios(BaseModel):
    """
    Pesos para cada criterio TOPSIS
    Todos los valores deben estar entre 0 y 1
    La suma total debe ser 1.0 (±0.01 tolerancia)
    """
    carga_laboral: float = Field(
        default=0.30,
        ge=0.0,
        le=1.0,
        description="Peso para carga laboral (menor carga = mejor)"
    )
    sesiones_completadas: float = Field(
        default=0.25,
        ge=0.0,
        le=1.0,
        description="Peso para sesiones completadas (más experiencia = mejor)"
    )
    rating: float = Field(
        default=0.30,
        ge=0.0,
        le=1.0,
        description="Peso para rating profesional (mayor rating = mejor)"
    )
    especialidad: float = Field(
        default=0.15,
        ge=0.0,
        le=1.0,
        description="Peso para especialidad (coincide con terapia = mejor)"
    )
    
    @model_validator(mode='after')
    def validar_suma_pesos(self):
        """Valida que la suma de todos los pesos sea 1.0"""
        suma = (
            self.carga_laboral + 
            self.sesiones_completadas + 
            self.rating + 
            self.especialidad
        )
        
        # Tolerancia de ±0.01 por redondeos
        if not (0.99 <= suma <= 1.01):
            raise ValueError(
                f"La suma de los pesos debe ser 1.0. Suma actual: {suma:.4f}"
            )
        
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "carga_laboral": 0.30,
                "sesiones_completadas": 0.25,
                "rating": 0.30,
                "especialidad": 0.15
            }
        }


class TopsisEvaluacionRequest(BaseModel):
    """Request para evaluar terapeutas con TOPSIS"""
    terapia_id: Optional[int] = Field(
        default=None,
        description="ID de terapia para filtrar por especialidad (opcional)"
    )
    pesos: PesosCriterios = Field(
        default_factory=PesosCriterios,
        description="Pesos para cada criterio TOPSIS"
    )
    incluir_inactivos: bool = Field(
        default=False,
        description="Incluir terapeutas con estado laboral inactivo"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "terapia_id": 10,
                "pesos": {
                    "carga_laboral": 0.30,
                    "sesiones_completadas": 0.25,
                    "rating": 0.30,
                    "especialidad": 0.15
                },
                "incluir_inactivos": False
            }
        }


class MetricasTerapeuta(BaseModel):
    """Métricas calculadas para un terapeuta"""
    carga_laboral: int = Field(description="Número de citas activas")
    sesiones_completadas: int = Field(description="Total de sesiones impartidas")
    rating: float = Field(description="Promedio de valoraciones (0-5)")
    especialidad_match: bool = Field(description="¿Domina la terapia solicitada?")
    
    class Config:
        json_schema_extra = {
            "example": {
                "carga_laboral": 8,
                "sesiones_completadas": 45,
                "rating": 4.5,
                "especialidad_match": True
            }
        }


class TerapeutaRanking(BaseModel):
    """Resultado TOPSIS para un terapeuta"""
    terapeuta_id: int = Field(description="ID del terapeuta")
    nombre: str = Field(description="Nombre completo del terapeuta")
    especialidad_principal: Optional[str] = Field(description="Especialidad principal")
    score: float = Field(
        ge=0.0,
        le=1.0,
        description="Score TOPSIS normalizado (0-1, mayor es mejor)"
    )
    ranking: int = Field(
        ge=1,
        description="Posición en el ranking (1 = mejor)"
    )
    metricas: MetricasTerapeuta = Field(description="Métricas detalladas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "terapeuta_id": 3,
                "nombre": "Ana Pérez García",
                "especialidad_principal": "Lenguaje y Comunicación",
                "score": 0.812,
                "ranking": 1,
                "metricas": {
                    "carga_laboral": 8,
                    "sesiones_completadas": 45,
                    "rating": 4.5,
                    "especialidad_match": True
                }
            }
        }


class TopsisResultado(BaseModel):
    """Respuesta completa del endpoint TOPSIS"""
    total_evaluados: int = Field(description="Total de terapeutas evaluados")
    terapia_solicitada: Optional[str] = Field(description="Nombre de la terapia filtrada")
    pesos_aplicados: PesosCriterios = Field(description="Pesos utilizados en el cálculo")
    ranking: list[TerapeutaRanking] = Field(description="Lista ordenada por score TOPSIS")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_evaluados": 5,
                "terapia_solicitada": "Terapia Conductual ABA",
                "pesos_aplicados": {
                    "carga_laboral": 0.30,
                    "sesiones_completadas": 0.25,
                    "rating": 0.30,
                    "especialidad": 0.15
                },
                "ranking": [
                    {
                        "terapeuta_id": 3,
                        "nombre": "Ana Pérez García",
                        "especialidad_principal": "Lenguaje y Comunicación",
                        "score": 0.812,
                        "ranking": 1,
                        "metricas": {
                            "carga_laboral": 8,
                            "sesiones_completadas": 45,
                            "rating": 4.5,
                            "especialidad_match": True
                        }
                    }
                ]
            }
        }
