"""
Endpoints para terapias, asignaciones y sesiones
"""

from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.usuario import Usuario
from app.schemas.terapia import (
    Terapia as TerapiaSchema,
    TerapiaCreate,
    TerapiaUpdate,
    TerapiaNino,
    TerapiaNinoCreate,
    TerapiaNinoUpdate,
    Sesion,
    SesionCreate,
    SesionUpdate,
    Reposicion,
    ReposicionCreate,
    ReposicionUpdate,
)
from app.services.terapia_service import terapia_service


router = APIRouter()


# ============= TERAPIAS =============

@router.get("/terapias", response_model=dict)
async def listar_terapias(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None, description="Buscar por nombre o descripción"),
    activo: Optional[bool] = Query(None, description="Filtrar por activo/inactivo"),
    tipo_id: Optional[int] = Query(None, description="Filtrar por tipo de terapia"),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("terapias:ver")),
):
    """
    Listar terapias con filtros y paginación.
    
    **Permisos requeridos:** `terapias:ver`
    """
    terapias = terapia_service.get_terapia_list(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        activo=activo,
        tipo_id=tipo_id,
    )
    
    total = terapia_service.count_terapias(
        db=db,
        search=search,
        activo=activo,
        tipo_id=tipo_id,
    )
    
    return {
        "items": terapias,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.post("/terapias", response_model=TerapiaSchema, status_code=status.HTTP_201_CREATED)
async def crear_terapia(
    terapia_data: TerapiaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("terapias:crear")),
):
    """
    Crear nueva terapia.
    
    **Permisos requeridos:** `terapias:crear`
    """
    return terapia_service.create_terapia(db=db, terapia_data=terapia_data)


@router.get("/terapias/{terapia_id}", response_model=TerapiaSchema)
async def obtener_terapia(
    terapia_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("terapias:ver")),
):
    """
    Obtener terapia por ID.
    
    **Permisos requeridos:** `terapias:ver`
    """
    return terapia_service.get_terapia_by_id(db=db, terapia_id=terapia_id)


@router.put("/terapias/{terapia_id}", response_model=TerapiaSchema)
async def actualizar_terapia(
    terapia_id: int,
    terapia_data: TerapiaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("terapias:editar")),
):
    """
    Actualizar terapia.
    
    **Permisos requeridos:** `terapias:editar`
    """
    return terapia_service.update_terapia(
        db=db,
        terapia_id=terapia_id,
        terapia_data=terapia_data,
    )


@router.delete("/terapias/{terapia_id}")
async def eliminar_terapia(
    terapia_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("terapias:eliminar")),
):
    """
    Eliminar terapia (soft delete).
    
    **Permisos requeridos:** `terapias:eliminar`
    """
    return terapia_service.delete_terapia(db=db, terapia_id=terapia_id)


# ============= ASIGNACIÓN PERSONAL <-> TERAPIA =============

@router.post("/terapias/{terapia_id}/personal/{personal_id}")
async def asignar_personal_terapia(
    terapia_id: int,
    personal_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("terapias:editar")),
):
    """
    Asignar personal a terapia.
    
    **Permisos requeridos:** `terapias:editar`
    """
    return terapia_service.asignar_personal_terapia(
        db=db,
        terapia_id=terapia_id,
        personal_id=personal_id,
    )


@router.delete("/terapias/{terapia_id}/personal/{personal_id}")
async def desasignar_personal_terapia(
    terapia_id: int,
    personal_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("terapias:editar")),
):
    """
    Desasignar personal de terapia.
    
    **Permisos requeridos:** `terapias:editar`
    """
    return terapia_service.desasignar_personal_terapia(
        db=db,
        terapia_id=terapia_id,
        personal_id=personal_id,
    )


# ============= ASIGNACIÓN NIÑO <-> TERAPIA =============

@router.get("/terapias/nino/{nino_id}", response_model=list)
async def obtener_terapias_nino(
    nino_id: int,
    activo: Optional[bool] = Query(None, description="Filtrar por activo/inactivo"),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("terapias:ver")),
):
    """
    Obtener terapias asignadas a un niño.
    
    **Permisos requeridos:** `terapias:ver`
    """
    return terapia_service.get_terapias_nino(
        db=db,
        nino_id=nino_id,
        activo=activo,
    )


@router.post("/terapias/asignar-nino", response_model=TerapiaNino, status_code=status.HTTP_201_CREATED)
async def asignar_terapia_nino(
    asignacion_data: TerapiaNinoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("terapias:asignar")),
):
    """
    Asignar terapia a niño con terapeuta.
    
    **Permisos requeridos:** `terapias:asignar`
    """
    return terapia_service.asignar_terapia_nino(
        db=db,
        asignacion_data=asignacion_data,
    )


@router.put("/terapias/asignaciones/{asignacion_id}", response_model=TerapiaNino)
async def actualizar_terapia_nino(
    asignacion_id: int,
    asignacion_data: TerapiaNinoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("terapias:editar")),
):
    """
    Actualizar asignación de terapia a niño.
    
    **Permisos requeridos:** `terapias:editar`
    """
    return terapia_service.update_terapia_nino(
        db=db,
        asignacion_id=asignacion_id,
        asignacion_data=asignacion_data,
    )


@router.delete("/terapias/asignaciones/{asignacion_id}")
async def eliminar_terapia_nino(
    asignacion_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("terapias:eliminar")),
):
    """
    Eliminar asignación de terapia a niño (soft delete).
    
    **Permisos requeridos:** `terapias:eliminar`
    """
    return terapia_service.delete_terapia_nino(db=db, asignacion_id=asignacion_id)


# ============= SESIONES =============

@router.get("/sesiones", response_model=list)
async def listar_sesiones(
    terapia_nino_id: Optional[int] = Query(None, description="Filtrar por asignación"),
    nino_id: Optional[int] = Query(None, description="Filtrar por niño"),
    fecha_desde: Optional[datetime] = Query(None, description="Fecha desde (YYYY-MM-DD)"),
    fecha_hasta: Optional[datetime] = Query(None, description="Fecha hasta (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("sesiones:ver")),
):
    """
    Listar sesiones con filtros.
    
    **Permisos requeridos:** `sesiones:ver`
    """
    return terapia_service.get_sesiones(
        db=db,
        terapia_nino_id=terapia_nino_id,
        nino_id=nino_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        skip=skip,
        limit=limit,
    )


@router.post("/sesiones", response_model=Sesion, status_code=status.HTTP_201_CREATED)
async def crear_sesion(
    sesion_data: SesionCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("sesiones:crear")),
):
    """
    Crear nueva sesión.
    
    **Permisos requeridos:** `sesiones:crear`
    """
    return terapia_service.create_sesion(db=db, sesion_data=sesion_data)


@router.get("/sesiones/{sesion_id}", response_model=Sesion)
async def obtener_sesion(
    sesion_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("sesiones:ver")),
):
    """
    Obtener sesión por ID.
    
    **Permisos requeridos:** `sesiones:ver`
    """
    return terapia_service.get_sesion_by_id(db=db, sesion_id=sesion_id)


@router.put("/sesiones/{sesion_id}", response_model=Sesion)
async def actualizar_sesion(
    sesion_id: int,
    sesion_data: SesionUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("sesiones:editar")),
):
    """
    Actualizar sesión.
    
    **Permisos requeridos:** `sesiones:editar`
    """
    return terapia_service.update_sesion(
        db=db,
        sesion_id=sesion_id,
        sesion_data=sesion_data,
    )


@router.delete("/sesiones/{sesion_id}")
async def eliminar_sesion(
    sesion_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("sesiones:eliminar")),
):
    """
    Eliminar sesión (hard delete).
    
    **Permisos requeridos:** `sesiones:eliminar`
    """
    return terapia_service.delete_sesion(db=db, sesion_id=sesion_id)


# ============= REPOSICIONES =============

@router.get("/reposiciones", response_model=list)
async def listar_reposiciones(
    nino_id: Optional[int] = Query(None, description="Filtrar por niño"),
    estado: Optional[str] = Query(None, description="PENDIENTE/APROBADA/RECHAZADA"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("reposiciones:ver")),
):
    """
    Listar reposiciones con filtros.
    
    **Permisos requeridos:** `reposiciones:ver`
    """
    return terapia_service.get_reposiciones(
        db=db,
        nino_id=nino_id,
        estado=estado,
        skip=skip,
        limit=limit,
    )


@router.post("/reposiciones", response_model=Reposicion, status_code=status.HTTP_201_CREATED)
async def crear_reposicion(
    reposicion_data: ReposicionCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("reposiciones:crear")),
):
    """
    Crear solicitud de reposición.
    
    **Permisos requeridos:** `reposiciones:crear`
    """
    return terapia_service.create_reposicion(db=db, reposicion_data=reposicion_data)


@router.put("/reposiciones/{reposicion_id}", response_model=Reposicion)
async def actualizar_reposicion(
    reposicion_id: int,
    reposicion_data: ReposicionUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("reposiciones:editar")),
):
    """
    Actualizar reposición.
    
    **Permisos requeridos:** `reposiciones:editar`
    """
    return terapia_service.update_reposicion(
        db=db,
        reposicion_id=reposicion_id,
        reposicion_data=reposicion_data,
    )


@router.post("/reposiciones/{reposicion_id}/aprobar", response_model=Reposicion)
async def aprobar_reposicion(
    reposicion_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("reposiciones:aprobar")),
):
    """
    Aprobar reposición.
    
    **Permisos requeridos:** `reposiciones:aprobar`
    """
    return terapia_service.aprobar_reposicion(db=db, reposicion_id=reposicion_id)


@router.post("/reposiciones/{reposicion_id}/rechazar", response_model=Reposicion)
async def rechazar_reposicion(
    reposicion_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("reposiciones:rechazar")),
):
    """
    Rechazar reposición.
    
    **Permisos requeridos:** `reposiciones:rechazar`
    """
    return terapia_service.rechazar_reposicion(db=db, reposicion_id=reposicion_id)
