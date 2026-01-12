from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/padre/sesiones", tags=["Padre - Sesiones"])

# ==================== MODELOS ====================

class Actividad(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    completada: bool
    observaciones: Optional[str] = None

class Sesion(BaseModel):
    id: int
    hijoId: int
    tipoTerapia: str
    fecha: str
    horaInicio: str
    horaFin: str
    terapeuta: Optional[str] = None
    estado: str  # 'completada', 'pendiente', 'cancelada'
    puntuacion: Optional[int] = None

class SesionDetalle(BaseModel):
    id: int
    hijoId: int
    tipoTerapia: str
    fecha: str
    horaInicio: str
    horaFin: str
    terapeuta: Optional[str] = None
    estado: str
    comentarios: Optional[str] = None
    grabacionUrl: Optional[str] = None
    bitacoraUrl: Optional[str] = None
    actividades: List[Actividad] = []
    puntuacion: Optional[int] = None

# ==================== ALMACENAMIENTO EN MEMORIA ====================

_sesiones_db: List[SesionDetalle] = [
    SesionDetalle(
        id=1,
        hijoId=1,
        tipoTerapia="Logopedia",
        fecha="2026-01-12",
        horaInicio="10:00",
        horaFin="11:00",
        terapeuta="María García",
        estado="completada",
        comentarios="Buena sesión, trabajo de pronunciación.",
        grabacionUrl=None,
        bitacoraUrl=None,
        actividades=[
            Actividad(id=1, nombre="Ejercicios de soplo", completada=True),
            Actividad(id=2, nombre="Lectura compartida", completada=True),
        ],
        puntuacion=8,
    ),
    SesionDetalle(
        id=2,
        hijoId=1,
        tipoTerapia="Terapia Ocupacional",
        fecha="2026-01-13",
        horaInicio="14:00",
        horaFin="15:00",
        terapeuta="Carlos López",
        estado="pendiente",
        comentarios=None,
        grabacionUrl=None,
        bitacoraUrl=None,
        actividades=[],
        puntuacion=None,
    ),
]

# ==================== ENDPOINTS ====================

@router.get("/hoy/{hijo_id}", response_model=List[Sesion])
def get_hoy(hijo_id: int):
    """Obtiene sesiones de hoy."""
    hoy = datetime.now().strftime("%Y-%m-%d")
    return [
        Sesion(
            id=s.id,
            hijoId=s.hijoId,
            tipoTerapia=s.tipoTerapia,
            fecha=s.fecha,
            horaInicio=s.horaInicio,
            horaFin=s.horaFin,
            terapeuta=s.terapeuta,
            estado=s.estado,
            puntuacion=s.puntuacion,
        )
        for s in _sesiones_db
        if s.hijoId == hijo_id and s.fecha == hoy
    ]

@router.get("/programadas/{hijo_id}", response_model=List[Sesion])
def get_programadas(hijo_id: int):
    """Obtiene sesiones futuras programadas."""
    hoy = datetime.now().strftime("%Y-%m-%d")
    return [
        Sesion(
            id=s.id,
            hijoId=s.hijoId,
            tipoTerapia=s.tipoTerapia,
            fecha=s.fecha,
            horaInicio=s.horaInicio,
            horaFin=s.horaFin,
            terapeuta=s.terapeuta,
            estado=s.estado,
            puntuacion=s.puntuacion,
        )
        for s in _sesiones_db
        if s.hijoId == hijo_id and s.fecha > hoy and s.estado == "pendiente"
    ]

@router.get("/semana/{hijo_id}", response_model=List[Sesion])
def get_semana(hijo_id: int):
    """Obtiene sesiones de esta semana."""
    hoy = datetime.now()
    fin_semana = (hoy + timedelta(days=7)).strftime("%Y-%m-%d")
    hoy_str = hoy.strftime("%Y-%m-%d")
    return [
        Sesion(
            id=s.id,
            hijoId=s.hijoId,
            tipoTerapia=s.tipoTerapia,
            fecha=s.fecha,
            horaInicio=s.horaInicio,
            horaFin=s.horaFin,
            terapeuta=s.terapeuta,
            estado=s.estado,
            puntuacion=s.puntuacion,
        )
        for s in _sesiones_db
        if s.hijoId == hijo_id and hoy_str <= s.fecha <= fin_semana
    ]

@router.get("/{sesion_id}", response_model=SesionDetalle)
def get_detalle(sesion_id: int):
    """Obtiene detalle completo de una sesión."""
    for s in _sesiones_db:
        if s.id == sesion_id:
            return s
    raise HTTPException(status_code=404, detail="Sesión no encontrada")

@router.get("/{sesion_id}/bitacora")
def get_bitacora(sesion_id: int):
    """Descarga la bitácora en PDF."""
    for s in _sesiones_db:
        if s.id == sesion_id:
            # Aquí iría la lógica de generar PDF o servir archivo
            # Por ahora retorna un mensaje
            return {"message": "Bitácora descargada"}
    raise HTTPException(status_code=404, detail="Sesión no encontrada")