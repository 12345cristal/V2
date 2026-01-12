# app/schemas/recurso.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ==================== TIPO RECURSO ====================

class TipoRecursoBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None


class TipoRecursoResponse(TipoRecursoBase):
    id: int
    
    class Config:
        from_attributes = True


# ==================== CATEGORIA RECURSO ====================

class CategoriaRecursoBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None


class CategoriaRecursoResponse(CategoriaRecursoBase):
    id: int
    
    class Config:
        from_attributes = True


# ==================== NIVEL RECURSO ====================

class NivelRecursoBase(BaseModel):
    codigo: str
    nombre: str
    orden: int = 0


class NivelRecursoResponse(NivelRecursoBase):
    id: int
    
    class Config:
        from_attributes = True


# ==================== RECURSO ====================

class RecursoBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    tipo_id: Optional[int] = None
    categoria_id: Optional[int] = None
    nivel_id: Optional[int] = None
    etiquetas: Optional[List[str]] = []
    archivo_url: Optional[str] = None
    es_destacado: int = 0


class RecursoCreate(RecursoBase):
    personal_id: Optional[int] = None


class RecursoUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = None
    tipo_id: Optional[int] = None
    categoria_id: Optional[int] = None
    nivel_id: Optional[int] = None
    etiquetas: Optional[List[str]] = None
    archivo_url: Optional[str] = None
    es_destacado: Optional[int] = None
    activo: Optional[int] = None


class RecursoResponse(RecursoBase):
    id: int
    personal_id: Optional[int]
    fecha_publicacion: datetime
    fecha_modificacion: datetime
    activo: int
    
    # Información adicional del personal
    personal_nombre: Optional[str] = None
    tipo_nombre: Optional[str] = None
    categoria_nombre: Optional[str] = None
    nivel_nombre: Optional[str] = None
    
    class Config:
        from_attributes = True


class RecursoListItem(BaseModel):
    """Versión simplificada para listados"""
    id: int
    titulo: str
    descripcion: Optional[str]
    tipo_nombre: Optional[str]
    categoria_nombre: Optional[str]
    nivel_nombre: Optional[str]
    es_destacado: int
    fecha_publicacion: datetime
    
    class Config:
        from_attributes = True
