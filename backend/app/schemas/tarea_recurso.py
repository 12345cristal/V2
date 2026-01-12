# app/schemas/tarea_recurso.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class TareaRecursoBase(BaseModel):
    recurso_id: int
    nino_id: int
    fecha_limite: Optional[date] = None
    notas_terapeuta: Optional[str] = None


class TareaRecursoCreate(TareaRecursoBase):
    asignado_por: Optional[int] = None


class TareaRecursoUpdate(BaseModel):
    fecha_limite: Optional[date] = None
    notas_terapeuta: Optional[str] = None
    completado: Optional[int] = None
    comentarios_padres: Optional[str] = None


class TareaRecursoMarcarCompletada(BaseModel):
    comentarios_padres: Optional[str] = None
    evidencia_url: Optional[str] = None
    evidencia_tipo: Optional[str] = None


class TareaRecursoResponse(TareaRecursoBase):
    id: int
    asignado_por: Optional[int]
    fecha_asignacion: datetime
    fecha_completado: Optional[datetime]
    completado: int
    comentarios_padres: Optional[str]
    evidencia_url: Optional[str]
    evidencia_tipo: Optional[str]
    
    # Información adicional del recurso
    recurso_titulo: Optional[str] = None
    recurso_descripcion: Optional[str] = None
    recurso_archivo_url: Optional[str] = None
    recurso_tipo: Optional[str] = None
    
    # Información del niño
    nino_nombre: Optional[str] = None
    nino_apellido: Optional[str] = None
    
    # Información del asignador
    asignador_nombre: Optional[str] = None
    
    class Config:
        from_attributes = True


class TareaRecursoListItem(BaseModel):
    """Versión simplificada para listados"""
    id: int
    recurso_id: int
    recurso_titulo: str
    recurso_tipo: Optional[str]
    nino_id: int
    nino_nombre: str
    fecha_asignacion: datetime
    fecha_limite: Optional[date]
    completado: int
    asignador_nombre: Optional[str]
    
    class Config:
        from_attributes = True


class EstadisticasTareasResponse(BaseModel):
    """Estadísticas de tareas de un niño"""
    total: int
    pendientes: int
    completadas: int
    vencidas: int
    porcentaje_completadas: float
