"""
Endpoints para citas y programación
"""

from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.usuario import Usuario
from app.schemas.cita import (
    Cita as CitaSchema,
    CitaCreate,
    CitaUpdate,
)
from app.services.cita_service import cita_service


router = APIRouter()


@router.get("/citas", response_model=dict)
async def listar_citas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    nino_id: Optional[int] = Query(None, description="Filtrar por niño"),
    terapeuta_id: Optional[int] = Query(None, description="Filtrar por terapeuta"),
    terapia_id: Optional[int] = Query(None, description="Filtrar por terapia"),
    fecha_desde: Optional[date] = Query(None, description="Fecha desde (YYYY-MM-DD)"),
    fecha_hasta: Optional[date] = Query(None, description="Fecha hasta (YYYY-MM-DD)"),
    estado_id: Optional[int] = Query(None, description="Filtrar por estado"),
    es_reposicion: Optional[bool] = Query(None, description="Solo reposiciones"),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("citas:ver")),
):
    """
    Listar citas con filtros y paginación.
    
    **Permisos requeridos:** `citas:ver`
    
    **Filtros disponibles:**
    - nino_id: Citas de un niño específico
    - terapeuta_id: Citas de un terapeuta específico
    - terapia_id: Citas de una terapia específica
    - fecha_desde/fecha_hasta: Rango de fechas
    - estado_id: Estado de la cita (1=Programada, 2=Completada, 3=Cancelada, 4=No asistió)
    - es_reposicion: true/false para filtrar reposiciones
    """
    citas = cita_service.get_cita_list(
        db=db,
        skip=skip,
        limit=limit,
        nino_id=nino_id,
        terapeuta_id=terapeuta_id,
        terapia_id=terapia_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        estado_id=estado_id,
        es_reposicion=es_reposicion,
    )
    
    total = cita_service.count_citas(
        db=db,
        nino_id=nino_id,
        terapeuta_id=terapeuta_id,
        terapia_id=terapia_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        estado_id=estado_id,
        es_reposicion=es_reposicion,
    )
    
    return {
        "items": citas,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.post("/citas", response_model=CitaSchema, status_code=status.HTTP_201_CREATED)
async def crear_cita(
    cita_data: CitaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("citas:crear")),
):
    """
    Crear nueva cita.
    
    **Permisos requeridos:** `citas:crear`
    
    **Validaciones:**
    - El niño, terapeuta y terapia deben existir
    - No puede haber conflictos de horario para el terapeuta
    - La hora_fin debe ser posterior a hora_inicio
    """
    return cita_service.create_cita(db=db, cita_data=cita_data)


@router.get("/citas/{cita_id}", response_model=CitaSchema)
async def obtener_cita(
    cita_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("citas:ver")),
):
    """
    Obtener cita por ID.
    
    **Permisos requeridos:** `citas:ver`
    """
    return cita_service.get_cita_by_id(db=db, cita_id=cita_id)


@router.put("/citas/{cita_id}", response_model=CitaSchema)
async def actualizar_cita(
    cita_id: int,
    cita_data: CitaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("citas:editar")),
):
    """
    Actualizar cita.
    
    **Permisos requeridos:** `citas:editar`
    
    **Validaciones:**
    - Si se cambia el horario, verifica conflictos
    """
    return cita_service.update_cita(
        db=db,
        cita_id=cita_id,
        cita_data=cita_data,
    )


@router.delete("/citas/{cita_id}")
async def eliminar_cita(
    cita_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("citas:eliminar")),
):
    """
    Eliminar cita (hard delete).
    
    **Permisos requeridos:** `citas:eliminar`
    """
    return cita_service.delete_cita(db=db, cita_id=cita_id)


@router.get("/citas/fecha/{fecha}")
async def obtener_citas_por_fecha(
    fecha: date,
    terapeuta_id: Optional[int] = Query(None, description="Filtrar por terapeuta"),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("citas:ver")),
):
    """
    Obtener citas de una fecha específica (vista de calendario).
    
    **Permisos requeridos:** `citas:ver`
    
    **Uso:** Para mostrar agenda diaria del centro o de un terapeuta.
    """
    return cita_service.get_citas_by_fecha(
        db=db,
        fecha=fecha,
        terapeuta_id=terapeuta_id,
    )


@router.post("/citas/{cita_id}/asistencia")
async def marcar_asistencia(
    cita_id: int,
    asistio: bool = Query(..., description="true=Asistió, false=No asistió"),
    observaciones: Optional[str] = Query(None, description="Observaciones adicionales"),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("citas:asistencia")),
):
    """
    Marcar asistencia de una cita.
    
    **Permisos requeridos:** `citas:asistencia`
    
    **Cambios:**
    - Si asistió: estado → Completada
    - Si no asistió: estado → No asistió
    """
    return cita_service.marcar_asistencia(
        db=db,
        cita_id=cita_id,
        asistio=asistio,
        observaciones=observaciones,
    )


@router.post("/citas/{cita_id}/cancelar")
async def cancelar_cita(
    cita_id: int,
    motivo: Optional[str] = Query(None, description="Motivo de cancelación"),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("citas:cancelar")),
):
    """
    Cancelar cita.
    
    **Permisos requeridos:** `citas:cancelar`
    
    **Cambios:** estado → Cancelada
    """
    return cita_service.cancelar_cita(
        db=db,
        cita_id=cita_id,
        motivo=motivo,
    )
