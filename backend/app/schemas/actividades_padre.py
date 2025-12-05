from pydantic import BaseModel
from datetime import datetime

class ActividadAsignadaPadre(BaseModel):
    id: int
    actividad_id: int
    nino_id: int
    nino_nombre: str

    actividad_titulo: str
    actividad_descripcion_corta: str | None
    objetivo_clinico: str | None
    instrucciones_padres: str | None
    material_requerido: str | None
    duracion_minutos: int | None

    fecha_asignacion: datetime
    fecha_limite: datetime | None
    completado: bool
    fecha_completado: datetime | None
