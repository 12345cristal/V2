from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, timedelta
from pathlib import Path

from app.db.session import get_db
from app.models.sesion import Sesion, EstadoSesion, ActividadSesion
from app.models.paciente import Paciente
from pydantic import BaseModel

router = APIRouter(prefix="/padre/sesiones", tags=["Padre - Sesiones"])

# ==================== MODELOS PYDANTIC ====================

class ActividadResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    completada: bool
    observaciones: Optional[str] = None
    
    class Config:
        from_attributes = True

class SesionResponse(BaseModel):
    id: int
    hijoId: int
    tipoTerapia: str
    fecha: str
    horaInicio: str
    horaFin: str
    terapeuta: Optional[str] = None
    estado: str
    puntuacion: Optional[int] = None
    
    class Config:
        from_attributes = True

class SesionDetalleResponse(BaseModel):
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
    actividades: List[ActividadResponse] = []
    puntuacion: Optional[int] = None
    
    class Config:
        from_attributes = True

# ==================== FUNCIONES AUXILIARES ====================

def sesion_to_response(sesion: Sesion) -> dict:
    """Convierte sesión a diccionario de respuesta."""
    return {
        "id": sesion.id,
        "hijoId": sesion.hijo_id,
        "tipoTerapia": sesion.tipo_terapia,
        "fecha": sesion.fecha,
        "horaInicio": sesion.hora_inicio,
        "horaFin": sesion.hora_fin,
        "terapeuta": sesion.terapeuta.nombre if sesion.terapeuta else None,
        "estado": sesion.estado.value,
        "puntuacion": sesion.puntuacion
    }

def sesion_detalle_to_response(sesion: Sesion) -> dict:
    """Convierte sesión con detalles a diccionario."""
    return {
        "id": sesion.id,
        "hijoId": sesion.hijo_id,
        "tipoTerapia": sesion.tipo_terapia,
        "fecha": sesion.fecha,
        "horaInicio": sesion.hora_inicio,
        "horaFin": sesion.hora_fin,
        "terapeuta": sesion.terapeuta.nombre if sesion.terapeuta else None,
        "estado": sesion.estado.value,
        "comentarios": sesion.comentarios,
        "grabacionUrl": sesion.grabacion_url,
        "bitacoraUrl": sesion.bitacora_url,
        "actividades": [
            {
                "id": a.id,
                "nombre": a.nombre,
                "descripcion": a.descripcion,
                "completada": a.completada,
                "observaciones": a.observaciones
            }
            for a in sesion.actividades
        ],
        "puntuacion": sesion.puntuacion
    }

def actualizar_estados_sesiones(db: Session, hijo_id: int):
    """Marca sesiones vencidas como canceladas automáticamente."""
    hoy = datetime.now().strftime("%Y-%m-%d")
    
    sesiones_vencidas = db.query(Sesion).filter(
        Sesion.hijo_id == hijo_id,
        Sesion.fecha < hoy,
        Sesion.estado == EstadoSesion.PENDIENTE
    ).all()
    
    for sesion in sesiones_vencidas:
        sesion.estado = EstadoSesion.CANCELADA
    
    if sesiones_vencidas:
        db.commit()

# ==================== ENDPOINTS ====================

@router.get("/hoy/{hijo_id}", response_model=List[SesionResponse])
def get_sesiones_hoy(hijo_id: int, db: Session = Depends(get_db)):
    """Obtiene sesiones de hoy."""
    hijo = db.query(Paciente).filter(Paciente.id == hijo_id).first()
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    hoy = datetime.now().strftime("%Y-%m-%d")
    
    sesiones = db.query(Sesion).filter(
        Sesion.hijo_id == hijo_id,
        Sesion.fecha == hoy
    ).options(joinedload(Sesion.terapeuta)).all()
    
    return [sesion_to_response(s) for s in sesiones]

@router.get("/programadas/{hijo_id}", response_model=List[SesionResponse])
def get_sesiones_programadas(hijo_id: int, db: Session = Depends(get_db)):
    """Obtiene sesiones futuras programadas."""
    hijo = db.query(Paciente).filter(Paciente.id == hijo_id).first()
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    hoy = datetime.now().strftime("%Y-%m-%d")
    
    sesiones = db.query(Sesion).filter(
        Sesion.hijo_id == hijo_id,
        Sesion.fecha > hoy,
        Sesion.estado == EstadoSesion.PENDIENTE
    ).options(joinedload(Sesion.terapeuta)).order_by(Sesion.fecha).all()
    
    return [sesion_to_response(s) for s in sesiones]

@router.get("/semana/{hijo_id}", response_model=List[SesionResponse])
def get_sesiones_semana(hijo_id: int, db: Session = Depends(get_db)):
    """Obtiene sesiones de esta semana."""
    hijo = db.query(Paciente).filter(Paciente.id == hijo_id).first()
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    hoy = datetime.now()
    fin_semana = hoy + timedelta(days=7)
    
    hoy_str = hoy.strftime("%Y-%m-%d")
    fin_semana_str = fin_semana.strftime("%Y-%m-%d")
    
    sesiones = db.query(Sesion).filter(
        Sesion.hijo_id == hijo_id,
        Sesion.fecha >= hoy_str,
        Sesion.fecha <= fin_semana_str
    ).options(joinedload(Sesion.terapeuta)).order_by(Sesion.fecha).all()
    
    return [sesion_to_response(s) for s in sesiones]

@router.get("/{sesion_id}", response_model=SesionDetalleResponse)
def get_sesion_detalle(sesion_id: int, db: Session = Depends(get_db)):
    """Obtiene detalle completo de una sesión."""
    sesion = db.query(Sesion).filter(Sesion.id == sesion_id).options(
        joinedload(Sesion.terapeuta),
        joinedload(Sesion.actividades)
    ).first()
    
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    return sesion_detalle_to_response(sesion)

@router.get("/{sesion_id}/bitacora")
def descargar_bitacora(sesion_id: int, db: Session = Depends(get_db)):
    """Descarga la bitácora de una sesión."""
    sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
    
    if not sesion or not sesion.bitacora_url:
        raise HTTPException(status_code=404, detail="Bitácora no encontrada")
    
    # Obtener ruta del archivo
    ruta = Path(sesion.bitacora_url.replace("http://localhost:8000/", ""))
    
    if not ruta.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    return FileResponse(ruta, filename=f"bitacora-{sesion_id}.pdf")