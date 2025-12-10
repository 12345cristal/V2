# backend/app/schemas/recomendacion_actividades.py
"""
Schemas para el sistema de recomendación de actividades basado en contenido
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ActividadRecomendadaBase(BaseModel):
    """Base para actividad recomendada"""
    actividad_id: int
    nombre: str
    descripcion: Optional[str] = None
    area_desarrollo: Optional[str] = None
    dificultad: int
    duracion_minutos: int


class ActividadRecomendada(ActividadRecomendadaBase):
    """Actividad con score de recomendación"""
    score_similitud: float = Field(
        ge=0.0,
        le=1.0,
        description="Score de similitud con el perfil del niño (0-1)"
    )
    ranking: int = Field(ge=1, description="Posición en el ranking")
    razon_recomendacion: str = Field(description="Explicación generada por IA")
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class RecomendacionRequest(BaseModel):
    """Request para obtener recomendaciones"""
    nino_id: int = Field(description="ID del niño")
    top_n: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Número de recomendaciones a retornar"
    )
    actualizar_perfil: bool = Field(
        default=False,
        description="Regenerar perfil del niño antes de recomendar"
    )
    filtrar_por_area: Optional[str] = Field(
        default=None,
        description="Filtrar por área de desarrollo (cognitivo, motor, lenguaje, social)"
    )
    nivel_dificultad_max: Optional[int] = Field(
        default=None,
        ge=1,
        le=3,
        description="Dificultad máxima permitida (1=Bajo, 2=Medio, 3=Alto)"
    )


class RecomendacionResponse(BaseModel):
    """Respuesta con recomendaciones"""
    nino_id: int
    nombre_nino: str
    total_recomendaciones: int
    perfil_actualizado: bool
    fecha_generacion: datetime
    recomendaciones: List[ActividadRecomendada]
    
    class Config:
        from_attributes = True


class PerfilNinoResponse(BaseModel):
    """Perfil del niño para visualización"""
    nino_id: int
    nombre_nino: str
    edad: Optional[int] = None
    diagnosticos: List[str] = Field(default_factory=list)
    dificultades: List[str] = Field(default_factory=list)
    fortalezas: List[str] = Field(default_factory=list)
    areas_prioritarias: List[str] = Field(default_factory=list)
    fecha_ultima_actualizacion: Optional[datetime] = None
    tiene_embedding: bool
    
    class Config:
        from_attributes = True


class ActualizarPerfilRequest(BaseModel):
    """Request para actualizar perfil manualmente"""
    nino_id: int
    forzar_regeneracion: bool = Field(
        default=False,
        description="Regenerar incluso si existe perfil reciente"
    )


class ProgresoActividadRequest(BaseModel):
    """Request para registrar progreso en actividad"""
    nino_id: int
    actividad_id: int
    terapeuta_id: int
    calificacion: float = Field(ge=1.0, le=5.0)
    notas_progreso: Optional[str] = None
    dificultad_encontrada: Optional[int] = Field(default=None, ge=1, le=3)


class ProgresoActividadResponse(BaseModel):
    """Response de progreso registrado"""
    id: int
    nino_id: int
    actividad_id: int
    calificacion: float
    fecha_registro: datetime
    
    class Config:
        from_attributes = True


class EstadisticasRecomendacionResponse(BaseModel):
    """Estadísticas del sistema de recomendación"""
    total_ninos_con_perfil: int
    total_actividades_vectorizadas: int
    total_recomendaciones_generadas: int
    promedio_score_similitud: float
    actividades_mas_recomendadas: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True
