"""
Schemas de Pydantic para Recursos, Tareas, Valoraciones y Recomendaciones
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# ============= RECURSO SCHEMAS =============

class RecursoBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    tipo_recurso_id: int
    categoria_recurso_id: int
    nivel_recurso_id: int
    nivel_dificultad_id: int
    url_recurso: Optional[str] = None
    duracion_minutos: Optional[int] = None
    instrucciones: Optional[str] = None
    objetivo: Optional[str] = None


class RecursoCreate(RecursoBase):
    pass


class RecursoUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_recurso_id: Optional[int] = None
    categoria_recurso_id: Optional[int] = None
    nivel_recurso_id: Optional[int] = None
    nivel_dificultad_id: Optional[int] = None
    url_recurso: Optional[str] = None
    duracion_minutos: Optional[int] = None
    instrucciones: Optional[str] = None
    objetivo: Optional[str] = None


class RecursoInDB(RecursoBase):
    id: int
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)


class RecursoWithDetails(RecursoInDB):
    """Recurso con nombres de catálogos"""
    tipo_recurso_nombre: Optional[str] = None
    categoria_recurso_nombre: Optional[str] = None
    nivel_recurso_nombre: Optional[str] = None
    nivel_dificultad_nombre: Optional[str] = None


class RecursoList(BaseModel):
    """Schema mínimo para listados"""
    id: int
    titulo: str
    tipo_recurso_nombre: Optional[str] = None
    categoria_recurso_nombre: Optional[str] = None
    nivel_recurso_nombre: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# ============= TAREA_RECURSO SCHEMAS =============

class TareaRecursoBase(BaseModel):
    recurso_id: int
    nino_id: int
    personal_id: int
    fecha_asignacion: datetime
    fecha_objetivo: Optional[datetime] = None
    completado: Optional[int] = 0
    fecha_completado: Optional[datetime] = None
    observaciones: Optional[str] = None


class TareaRecursoCreate(BaseModel):
    recurso_id: int
    nino_id: int
    fecha_objetivo: Optional[datetime] = None
    observaciones: Optional[str] = None


class TareaRecursoUpdate(BaseModel):
    fecha_objetivo: Optional[datetime] = None
    completado: Optional[int] = None
    fecha_completado: Optional[datetime] = None
    observaciones: Optional[str] = None


class TareaRecursoInDB(TareaRecursoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class TareaRecursoWithDetails(TareaRecursoInDB):
    """Tarea con detalles de recurso y niño"""
    recurso_titulo: Optional[str] = None
    nino_nombre: Optional[str] = None
    terapeuta_nombre: Optional[str] = None


# ============= VALORACION SCHEMAS =============

class ValoracionBase(BaseModel):
    recurso_id: int
    usuario_id: int
    puntuacion: int  # 1-5 estrellas
    comentario: Optional[str] = None


class ValoracionCreate(ValoracionBase):
    pass


class ValoracionUpdate(BaseModel):
    puntuacion: Optional[int] = None
    comentario: Optional[str] = None


class ValoracionInDB(ValoracionBase):
    id: int
    fecha_valoracion: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ValoracionWithUsuario(ValoracionInDB):
    """Valoración con nombre de usuario"""
    usuario_nombre: Optional[str] = None


# ============= RECOMENDACION SCHEMAS =============

class RecomendacionBase(BaseModel):
    nino_id: int
    recurso_id: int
    prioridad_id: int
    motivo: Optional[str] = None
    generado_por_ia: Optional[int] = 0


class RecomendacionCreate(RecomendacionBase):
    pass


class RecomendacionUpdate(BaseModel):
    prioridad_id: Optional[int] = None
    motivo: Optional[str] = None


class RecomendacionInDB(RecomendacionBase):
    id: int
    fecha_recomendacion: datetime
    
    model_config = ConfigDict(from_attributes=True)


class RecomendacionWithDetails(RecomendacionInDB):
    """Recomendación con detalles"""
    recurso_titulo: Optional[str] = None
    nino_nombre: Optional[str] = None
    prioridad_nombre: Optional[str] = None
