"""
Endpoints para niños - Módulo más complejo con 5 tablas relacionadas
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.usuario import Usuario
from app.schemas.nino import (
    NinoInDB,
    NinoCreate,
    NinoUpdate,
    NinoDireccionInDB,
    NinoDireccionCreate,
    NinoDireccionUpdate,
    NinoDiagnosticoInDB,
    NinoDiagnosticoCreate,
    NinoDiagnosticoUpdate,
    NinoInfoEmocionalInDB,
    NinoInfoEmocionalCreate,
    NinoInfoEmocionalUpdate,
    NinoArchivosInDB,
    NinoArchivosCreate,
    NinoArchivosUpdate,
)
from app.services.nino_service import nino_service


router = APIRouter()


# ============= ENDPOINTS BASE (NIÑO) =============

@router.get("/ninos", response_model=dict)
async def listar_ninos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None, description="Buscar por nombre o CURP"),
    estado: Optional[str] = Query(None, description="ACTIVO/BAJA_TEMPORAL/INACTIVO"),
    tutor_id: Optional[int] = Query(None, description="Filtrar por tutor"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    """
    Listar niños con filtros y paginación.
    
    **Permisos requeridos:** `ninos:ver`
    """
    try:
        ninos = nino_service.get_nino_list(
            db=db,
            skip=skip,
            limit=limit,
            search=search,
            estado=estado,
            tutor_id=tutor_id,
        )
        
        total = nino_service.count_ninos(
            db=db,
            search=search,
            estado=estado,
            tutor_id=tutor_id,
        )
        
        return {
            "items": ninos,
            "total": total,
            "skip": skip,
            "limit": limit,
        }
    except Exception as e:
        print(f"❌ Error al listar niños: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener lista de niños: {str(e)}"
        )


@router.post("/ninos", response_model=NinoInDB, status_code=status.HTTP_201_CREATED)
async def crear_nino(
    nino_data: NinoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:crear")),
):
    """
    Crear nuevo niño.
    
    **Permisos requeridos:** `ninos:crear`
    """
    return nino_service.create_nino(db=db, nino_data=nino_data)


@router.get("/ninos/{nino_id}", response_model=NinoInDB)
async def obtener_nino(
    nino_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:ver")),
):
    """
    Obtener niño por ID con todas sus relaciones.
    
    **Permisos requeridos:** `ninos:ver`
    """
    return nino_service.get_nino_by_id(db=db, nino_id=nino_id)


@router.put("/ninos/{nino_id}", response_model=NinoInDB)
async def actualizar_nino(
    nino_id: int,
    nino_data: NinoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:editar")),
):
    """
    Actualizar niño.
    
    **Permisos requeridos:** `ninos:editar`
    """
    return nino_service.update_nino(
        db=db,
        nino_id=nino_id,
        nino_data=nino_data,
    )


@router.delete("/ninos/{nino_id}")
async def eliminar_nino(
    nino_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:eliminar")),
):
    """
    Eliminar niño (soft delete).
    
    **Permisos requeridos:** `ninos:eliminar`
    """
    return nino_service.delete_nino(db=db, nino_id=nino_id)


# ============= DIRECCIÓN =============

@router.get("/ninos/{nino_id}/direccion", response_model=NinoDireccionInDB)
async def obtener_direccion(
    nino_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:ver")),
):
    """
    Obtener dirección del niño.
    
    **Permisos requeridos:** `ninos:ver`
    """
    direccion = nino_service.get_direccion_by_nino(db=db, nino_id=nino_id)
    
    if not direccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El niño {nino_id} no tiene dirección registrada",
        )
    
    return direccion


@router.post("/ninos/{nino_id}/direccion", response_model=NinoDireccionInDB, status_code=status.HTTP_201_CREATED)
async def crear_direccion(
    nino_id: int,
    direccion_data: NinoDireccionCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:editar")),
):
    """
    Crear dirección del niño.
    
    **Permisos requeridos:** `ninos:editar`
    """
    return nino_service.create_direccion(
        db=db,
        nino_id=nino_id,
        direccion_data=direccion_data,
    )


@router.put("/ninos/{nino_id}/direccion", response_model=NinoDireccionInDB)
async def actualizar_direccion(
    nino_id: int,
    direccion_data: NinoDireccionUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:editar")),
):
    """
    Actualizar dirección del niño.
    
    **Permisos requeridos:** `ninos:editar`
    """
    return nino_service.update_direccion(
        db=db,
        nino_id=nino_id,
        direccion_data=direccion_data,
    )


# ============= DIAGNÓSTICO =============

@router.get("/ninos/{nino_id}/diagnostico", response_model=NinoDiagnosticoInDB)
async def obtener_diagnostico(
    nino_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:ver")),
):
    """
    Obtener diagnóstico del niño.
    
    **Permisos requeridos:** `ninos:ver`
    """
    diagnostico = nino_service.get_diagnostico_by_nino(db=db, nino_id=nino_id)
    
    if not diagnostico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El niño {nino_id} no tiene diagnóstico registrado",
        )
    
    return diagnostico


@router.post("/ninos/{nino_id}/diagnostico", response_model=NinoDiagnosticoInDB, status_code=status.HTTP_201_CREATED)
async def crear_diagnostico(
    nino_id: int,
    diagnostico_data: NinoDiagnosticoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:editar")),
):
    """
    Crear diagnóstico del niño.
    
    **Permisos requeridos:** `ninos:editar`
    """
    return nino_service.create_diagnostico(
        db=db,
        nino_id=nino_id,
        diagnostico_data=diagnostico_data,
    )


@router.put("/ninos/{nino_id}/diagnostico", response_model=NinoDiagnosticoInDB)
async def actualizar_diagnostico(
    nino_id: int,
    diagnostico_data: NinoDiagnosticoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:editar")),
):
    """
    Actualizar diagnóstico del niño.
    
    **Permisos requeridos:** `ninos:editar`
    """
    return nino_service.update_diagnostico(
        db=db,
        nino_id=nino_id,
        diagnostico_data=diagnostico_data,
    )


# ============= INFO EMOCIONAL =============

@router.get("/ninos/{nino_id}/info-emocional", response_model=NinoInfoEmocionalInDB)
async def obtener_info_emocional(
    nino_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:ver")),
):
    """
    Obtener información emocional del niño.
    
    **Permisos requeridos:** `ninos:ver`
    """
    info = nino_service.get_info_emocional_by_nino(db=db, nino_id=nino_id)
    
    if not info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El niño {nino_id} no tiene info emocional registrada",
        )
    
    return info


@router.post("/ninos/{nino_id}/info-emocional", response_model=NinoInfoEmocionalInDB, status_code=status.HTTP_201_CREATED)
async def crear_info_emocional(
    nino_id: int,
    info_data: NinoInfoEmocionalCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:editar")),
):
    """
    Crear información emocional del niño.
    
    **Permisos requeridos:** `ninos:editar`
    """
    return nino_service.create_info_emocional(
        db=db,
        nino_id=nino_id,
        info_data=info_data,
    )


@router.put("/ninos/{nino_id}/info-emocional", response_model=NinoInfoEmocionalInDB)
async def actualizar_info_emocional(
    nino_id: int,
    info_data: NinoInfoEmocionalUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:editar")),
):
    """
    Actualizar información emocional del niño.
    
    **Permisos requeridos:** `ninos:editar`
    """
    return nino_service.update_info_emocional(
        db=db,
        nino_id=nino_id,
        info_data=info_data,
    )


# ============= ARCHIVOS =============

@router.get("/ninos/{nino_id}/archivos", response_model=NinoArchivosInDB)
async def obtener_archivos(
    nino_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:ver")),
):
    """
    Obtener archivos del niño.
    
    **Permisos requeridos:** `ninos:ver`
    """
    archivos = nino_service.get_archivos_by_nino(db=db, nino_id=nino_id)
    
    if not archivos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El niño {nino_id} no tiene archivos registrados",
        )
    
    return archivos


@router.post("/ninos/{nino_id}/archivos", response_model=NinoArchivosInDB, status_code=status.HTTP_201_CREATED)
async def crear_archivos(
    nino_id: int,
    archivos_data: NinoArchivosCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:editar")),
):
    """
    Crear registro de archivos del niño.
    
    **Permisos requeridos:** `ninos:editar`
    """
    return nino_service.create_archivos(
        db=db,
        nino_id=nino_id,
        archivos_data=archivos_data,
    )


@router.put("/ninos/{nino_id}/archivos", response_model=NinoArchivosInDB)
async def actualizar_archivos(
    nino_id: int,
    archivos_data: NinoArchivosUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:editar")),
):
    """
    Actualizar archivos del niño.
    
    **Permisos requeridos:** `ninos:editar`
    """
    return nino_service.update_archivos(
        db=db,
        nino_id=nino_id,
        archivos_data=archivos_data,
    )
