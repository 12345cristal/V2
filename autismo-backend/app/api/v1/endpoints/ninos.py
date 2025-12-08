# app/api/v1/endpoints/ninos.py
"""
Endpoints para niños - CRUD + 4 tablas relacionadas
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


# 👉 ESTE prefix ES EL CORRECTO
router = APIRouter(prefix="/ninos", tags=["Niños"])


# ===============================
# LISTAR NIÑOS
# ===============================
@router.get("/", response_model=dict)
async def listar_ninos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    estado: Optional[str] = None,
    tutor_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    try:
        items = nino_service.get_nino_list(
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

        return {"items": items, "total": total, "skip": skip, "limit": limit}

    except Exception as e:
        raise HTTPException(500, f"Error al obtener niños: {str(e)}")


# ===============================
# CREAR NIÑO
# ===============================
@router.post("/", response_model=NinoInDB, status_code=201)
async def crear_nino(
    nino_data: NinoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("ninos:crear")),
):
    return nino_service.create_nino(db, nino_data)


# ===============================
# OBTENER POR ID
# ===============================
@router.get("/{nino_id}", response_model=NinoInDB)
async def obtener_nino(
    nino_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    return nino_service.get_nino_by_id(db, nino_id)


# ===============================
# ACTUALIZAR
# ===============================
@router.put("/{nino_id}", response_model=NinoInDB)
async def actualizar_nino(
    nino_id: int,
    nino_data: NinoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    return nino_service.update_nino(db, nino_id, nino_data)


# ===============================
# ELIMINAR (soft)
# ===============================
@router.delete("/{nino_id}")
async def eliminar_nino(
    nino_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    return nino_service.delete_nino(db, nino_id)


# ===============================
# DIRECCIÓN
# ===============================
@router.get("/{nino_id}/direccion", response_model=NinoDireccionInDB)
async def obtener_direccion(
    nino_id: int,
    db: Session = Depends(get_db),
):
    return nino_service.get_direccion_by_nino(db, nino_id)


@router.post("/{nino_id}/direccion", response_model=NinoDireccionInDB, status_code=201)
async def crear_direccion(
    nino_id: int,
    data: NinoDireccionCreate,
    db: Session = Depends(get_db),
):
    return nino_service.create_direccion(db, nino_id, data)


@router.put("/{nino_id}/direccion", response_model=NinoDireccionInDB)
async def actualizar_direccion(
    nino_id: int,
    data: NinoDireccionUpdate,
    db: Session = Depends(get_db),
):
    return nino_service.update_direccion(db, nino_id, data)


# ===============================
# DIAGNOSTICO
# ===============================
@router.get("/{nino_id}/diagnostico", response_model=NinoDiagnosticoInDB)
async def obtener_diagnostico(
    nino_id: int,
    db: Session = Depends(get_db),
):
    return nino_service.get_diagnostico_by_nino(db, nino_id)


@router.post("/{nino_id}/diagnostico", response_model=NinoDiagnosticoInDB, status_code=201)
async def crear_diagnostico(
    nino_id: int,
    data: NinoDiagnosticoCreate,
    db: Session = Depends(get_db),
):
    return nino_service.create_diagnostico(db, nino_id, data)


@router.put("/{nino_id}/diagnostico", response_model=NinoDiagnosticoInDB)
async def actualizar_diagnostico(
    nino_id: int,
    data: NinoDiagnosticoUpdate,
    db: Session = Depends(get_db),
):
    return nino_service.update_diagnostico(db, nino_id, data)


# ===============================
# INFO EMOCIONAL
# ===============================
@router.get("/{nino_id}/info-emocional", response_model=NinoInfoEmocionalInDB)
async def obtener_info_emocional(
    nino_id: int,
    db: Session = Depends(get_db),
):
    return nino_service.get_info_emocional_by_nino(db, nino_id)


@router.post("/{nino_id}/info-emocional", response_model=NinoInfoEmocionalInDB, status_code=201)
async def crear_info_emocional(
    nino_id: int,
    data: NinoInfoEmocionalCreate,
    db: Session = Depends(get_db),
):
    return nino_service.create_info_emocional(db, nino_id, data)


@router.put("/{nino_id}/info-emocional", response_model=NinoInfoEmocionalInDB)
async def actualizar_info_emocional(
    nino_id: int,
    data: NinoInfoEmocionalUpdate,
    db: Session = Depends(get_db),
):
    return nino_service.update_info_emocional(db, nino_id, data)


# ===============================
# ARCHIVOS
# ===============================
@router.get("/{nino_id}/archivos", response_model=NinoArchivosInDB)
async def obtener_archivos(
    nino_id: int,
    db: Session = Depends(get_db),
):
    return nino_service.get_archivos_by_nino(db, nino_id)


@router.post("/{nino_id}/archivos", response_model=NinoArchivosInDB, status_code=201)
async def crear_archivos(
    nino_id: int,
    data: NinoArchivosCreate,
    db: Session = Depends(get_db),
):
    return nino_service.create_archivos(db, nino_id, data)


@router.put("/{nino_id}/archivos", response_model=NinoArchivosInDB)
async def actualizar_archivos(
    nino_id: int,
    data: NinoArchivosUpdate,
    db: Session = Depends(get_db),
):
    return nino_service.update_archivos(db, nino_id, data)
