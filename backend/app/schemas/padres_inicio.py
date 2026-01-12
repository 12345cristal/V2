from pydantic import BaseModel
from typing import Optional

class HijoResumen(BaseModel):
    id: str
    nombre: str
    edad: int
    fotoPerfil: Optional[str]
    estado: str

class ProximaSesionSchema(BaseModel):
    id: str
    fecha: str
    hora: str
    tipo: str
    terapeuta: str
    estado: str

class UltimoAvanceSchema(BaseModel):
    id: str
    fecha: str
    descripcion: str
    porcentaje: int
    area: str

class UltimaObservacionSchema(BaseModel):
    id: str
    fecha: str
    terapeuta: str
    resumen: str

class InicioPadreResponse(BaseModel):
    hijoSeleccionado: HijoResumen
    hijosActivos: list[HijoResumen]
    proximaSesion: Optional[ProximaSesionSchema]
    ultimoAvance: Optional[UltimoAvanceSchema]
    pagosPendientes: int
    documentosNuevos: int
    ultimaObservacion: Optional[UltimaObservacionSchema]
    porcentajeProgreso: int

    class Config:
        from_attributes = True
