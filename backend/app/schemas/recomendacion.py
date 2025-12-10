# app/schemas/recomendacion.py
from pydantic import BaseModel, Field
from typing import List


# ============================================================
# SCHEMAS PARA ACTIVIDADES
# ============================================================

class ActividadBase(BaseModel):
    """Base schema para Actividad"""
    nombre: str = Field(..., max_length=150)
    descripcion: str | None = None
    objetivo: str | None = None
    materiales: str | None = None
    duracion_minutos: int = Field(30, ge=1)
    tags: List[str] = Field(default_factory=list)
    dificultad: int = Field(1, ge=1, le=3)
    area_desarrollo: str | None = Field(None, max_length=100)
    activo: int = Field(1)


class ActividadCreate(ActividadBase):
    """Schema para crear una actividad"""
    pass


class ActividadUpdate(BaseModel):
    """Schema para actualizar una actividad"""
    nombre: str | None = None
    descripcion: str | None = None
    objetivo: str | None = None
    materiales: str | None = None
    duracion_minutos: int | None = None
    tags: List[str] | None = None
    dificultad: int | None = None
    area_desarrollo: str | None = None
    activo: int | None = None


class ActividadRead(ActividadBase):
    """Schema para leer una actividad"""
    id: int

    class Config:
        from_attributes = True


# ============================================================
# SCHEMAS PARA RECOMENDACIONES
# ============================================================

class RecomendacionActividad(BaseModel):
    """
    Recomendación de actividad con score de similitud
    """
    actividad_id: int = Field(..., description="ID de la actividad recomendada")
    nombre: str = Field(..., description="Nombre de la actividad")
    descripcion: str | None = Field(None, description="Descripción de la actividad")
    score: float = Field(..., description="Score de similitud (0-1)")
    tags: List[str] = Field(default_factory=list, description="Tags de la actividad")
    dificultad: int = Field(..., description="Nivel de dificultad")
    area_desarrollo: str | None = Field(None, description="Área de desarrollo")

    class Config:
        from_attributes = True


class RecomendacionTerapia(BaseModel):
    """
    Recomendación de terapia con score de similitud
    """
    terapia_id: int = Field(..., description="ID de la terapia recomendada")
    nombre: str = Field(..., description="Nombre de la terapia")
    descripcion: str | None = Field(None, description="Descripción de la terapia")
    score: float = Field(..., description="Score de similitud (0-1)")
    categoria: str | None = Field(None, description="Categoría de la terapia")
    tags: List[str] = Field(default_factory=list, description="Tags de la terapia")

    class Config:
        from_attributes = True


# ============================================================
# SCHEMAS PARA SISTEMA COMPLETO DE RECOMENDACIONES
# ============================================================

class RecomendacionActividadesResponse(BaseModel):
    """Respuesta del endpoint de recomendación de actividades"""
    nino_id: int
    recomendaciones: List[RecomendacionActividad]
    explicacion: str | None = None
    fecha_generacion: str


class TerapeutaRecomendado(BaseModel):
    """Schema para terapeuta recomendado por TOPSIS"""
    id: int
    nombre: str
    especialidad: str
    experiencia_anos: int
    score: float = Field(..., ge=0, le=1, description="Score TOPSIS")
    posicion: int
    carga_trabajo: int | None = None
    evaluacion: float | None = None


class SeleccionTerapeutaResponse(BaseModel):
    """Respuesta del endpoint de selección de terapeuta"""
    nino_id: int
    terapia_tipo: str
    terapeuta_seleccionado: TerapeutaRecomendado
    ranking_completo: List[TerapeutaRecomendado]
    explicacion: str | None = None
    criterios_usados: dict


class RecomendacionCompletaResponse(BaseModel):
    """Respuesta del flujo completo de recomendación"""
    nino: dict
    actividades_recomendadas: RecomendacionActividadesResponse
    terapeuta_asignado: SeleccionTerapeutaResponse
    fecha_generacion: str


class GenerarPerfilRequest(BaseModel):
    """Request para generar o actualizar perfil vectorizado"""
    nino_id: int
    forzar_actualizacion: bool = False


class RegistrarProgresoRequest(BaseModel):
    """Request para registrar progreso en actividad"""
    nino_id: int
    actividad_id: int
    terapeuta_id: int
    calificacion: float = Field(..., ge=1, le=5)
    notas_progreso: str | None = None
    duracion_minutos: int | None = None


class SugerenciaClinicaRequest(BaseModel):
    """Request para generar sugerencias clínicas con Gemini"""
    nino_id: int
    incluir_actividades_actuales: bool = True
    incluir_progreso_reciente: bool = True


class SugerenciaClinicaResponse(BaseModel):
    """Respuesta con sugerencias clínicas generadas por Gemini"""
    nino_id: int
    sugerencias: str
    contexto_usado: dict
    fecha_generacion: str
