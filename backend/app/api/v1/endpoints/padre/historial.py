# app/api/v1/endpoints/padre/historial.py
"""
Router para Historial Terapéutico desde el módulo Padre
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional

from app.api.deps import get_db_session, require_padre
from app.models.usuario import Usuario
from app.models.tutor import Tutor
from app.models.nino import Nino
from app.schemas.padre import HistorialTerapeutico, AsistenciaMes, EvolucionObjetivo


router = APIRouter()


def verificar_acceso_hijo(hijo_id: int, current_user: Usuario, db: Session) -> Nino:
    """Helper para verificar que el padre tenga acceso al hijo"""
    hijo = db.query(Nino).filter(Nino.id == hijo_id).first()
    if not hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    
    if current_user.rol_id == 4:
        tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
        if not tutor or hijo.tutor_id != tutor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para acceder a esta información"
            )
    
    return hijo


@router.get("/historial/{hijo_id}", response_model=HistorialTerapeutico)
async def obtener_historial(
    hijo_id: int,
    periodo: str = Query("mes", pattern="^(mes|trimestre|semestre|año)$"),
    mes: Optional[int] = Query(None, ge=1, le=12),
    año: Optional[int] = Query(None, ge=2020, le=2030),
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene datos del historial terapéutico para gráficas
    """
    hijo = verificar_acceso_hijo(hijo_id, current_user, db)
    
    # Calcular fechas según período
    hoy = date.today()
    año_ref = año or hoy.year
    mes_ref = mes or hoy.month
    
    # TODO: Implementar lógica real de cálculo de historial
    fecha_inicio = date(año_ref, mes_ref, 1)
    fecha_fin = hoy
    
    return HistorialTerapeutico(
        hijo_id=hijo_id,
        hijo_nombre=f"{hijo.nombre} {hijo.apellido_paterno}",
        periodo=periodo.upper(),
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        asistencia=[],
        evolucion_objetivos=[],
        total_sesiones=0,
        progreso_general=0
    )


@router.get("/historial/{hijo_id}/asistencia")
async def obtener_asistencia(
    hijo_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene asistencia por mes del hijo
    """
    hijo = verificar_acceso_hijo(hijo_id, current_user, db)
    
    # TODO: Implementar lógica real
    return {"message": "Funcionalidad en desarrollo"}


@router.get("/historial/{hijo_id}/evolucion")
async def obtener_evolucion(
    hijo_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene evolución de objetivos del hijo
    """
    hijo = verificar_acceso_hijo(hijo_id, current_user, db)
    
    # TODO: Implementar lógica real
    return {"message": "Funcionalidad en desarrollo"}


@router.get("/historial/{hijo_id}/frecuencia")
async def obtener_frecuencia(
    hijo_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene frecuencia de terapias del hijo
    """
    hijo = verificar_acceso_hijo(hijo_id, current_user, db)
    
    # TODO: Implementar lógica real
    return {"message": "Funcionalidad en desarrollo"}


@router.get("/historial/{hijo_id}/reporte")
async def descargar_reporte(
    hijo_id: int,
    periodo: str = Query("mes", pattern="^(mes|trimestre|semestre|año)$"),
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Descarga reporte del historial en PDF
    """
    hijo = verificar_acceso_hijo(hijo_id, current_user, db)
    
    # TODO: Implementar generación de PDF
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad de reporte PDF en desarrollo"
    )
