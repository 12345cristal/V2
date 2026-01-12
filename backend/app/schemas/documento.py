# app/schemas/documento.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TipoDocumentoEnum(str, Enum):
    ACUERDO_SERVICIOS = "ACUERDO_SERVICIOS"
    REPORTE_TERAPEUTICO = "REPORTE_TERAPEUTICO"
    DOCUMENTO_MEDICO = "DOCUMENTO_MEDICO"
    ACTUALIZACION_MEDICAMENTOS = "ACTUALIZACION_MEDICAMENTOS"
    OTRO = "OTRO"


class DocumentoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    descripcion: Optional[str] = None
    tipo_documento: TipoDocumentoEnum


class DocumentoCreate(DocumentoBase):
    pass


class DocumentoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_documento: Optional[TipoDocumentoEnum] = None


class DocumentoResponse(DocumentoBase):
    id: int
    key: Optional[int] = None  # Para compatibilidad con frontend
    nino_id: int
    url: str = Field(alias="url_archivo")
    nuevo: bool
    visto: bool = False
    tamanio_bytes: Optional[int] = None
    fecha_subida: datetime
    subido_por: Optional[str] = None
    tipo_archivo: str = "application/pdf"
    
    class Config:
        from_attributes = True
        populate_by_name = True
    
    @classmethod
    def from_orm(cls, db_obj):
        data = {
            "id": db_obj.id,
            "key": db_obj.id,
            "nombre": db_obj.nombre,
            "descripcion": db_obj.descripcion,
            "tipo_documento": db_obj.tipo_documento,
            "nino_id": db_obj.nino_id,
            "url_archivo": db_obj.url_archivo,
            "nuevo": db_obj.nuevo,
            "tamanio_bytes": db_obj.tamanio_bytes,
            "fecha_subida": db_obj.fecha_subida,
            "tipo_archivo": db_obj.tipo_archivo,
            "subido_por": db_obj.usuario.nombres if db_obj.usuario else None,
            "visto": any(v.visto for v in db_obj.vistos) if db_obj.vistos else False
        }
        return cls(**data)


class DocumentoDetalle(DocumentoResponse):
    fecha_actualizacion: datetime
    ruta_descarga: str = Field(default="")


class RespuestaDocumentos(BaseModel):
    success: bool
    data: List[DocumentoResponse] = []
    total: int = 0
    error: Optional[str] = None
    mensaje: Optional[str] = None