from pydantic import BaseModel
from datetime import datetime

class RecursoBase(BaseModel):
    id: int
    titulo: str
    descripcion: str | None
    tipo_id: int | None
    categoria_id: int | None
    nivel_id: int | None
    etiquetas: str | None
    es_destacado: bool
    es_nuevo: bool
    fecha_publicacion: datetime
    rating_promedio: float | None


class RecursoTareaRead(BaseModel):
    id: int
    recurso_id: int
    nino_id: int
    fecha_asignacion: datetime
    fecha_limite: datetime | None
    completado: bool
    comentarios_padres: str | None
    notas_terapeuta: str | None
