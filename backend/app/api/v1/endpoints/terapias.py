from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.schemas.terapia import (
    TerapiaSchema,
    TerapiaCreateRequest,
    TerapiaUpdateRequest,
    PersonalAsignadoSchema,
    AsignarPersonalRequest
)
from app.services.terapias_service import TerapiasService

router = APIRouter(
    prefix="/terapias",
    tags=["terapias"],
    dependencies=[Depends(get_current_active_user)]
)

# ============================================================
# GET — TODAS LAS TERAPIAS
# ============================================================
@router.get("/", response_model=list[TerapiaSchema])
def listar_terapias(db: Session = Depends(get_db)):
    return TerapiasService.listar(db)


# ============================================================
# GET — PERSONAL DISPONIBLE
# ============================================================
@router.get("/personal-disponible")
def personal_disponible(db: Session = Depends(get_db)):
    return TerapiasService.personal_disponible(db)


# ============================================================
# GET — PERSONAL ASIGNADO A TERAPIAS
# ============================================================
@router.get("/personal-asignado", response_model=list[PersonalAsignadoSchema])
def personal_asignado(db: Session = Depends(get_db)):
    return TerapiasService.personal_asignado(db)


# ============================================================
# POST — CREAR TERAPIA
# ============================================================
@router.post("/", response_model=TerapiaSchema)
def crear_terapia(dto: TerapiaCreateRequest, db: Session = Depends(get_db)):
    return TerapiasService.crear(dto.dict(), db)


# ============================================================
# PUT — ACTUALIZAR TERAPIA
# ============================================================
@router.put("/{id}", response_model=TerapiaSchema)
def actualizar_terapia(id: int, dto: TerapiaUpdateRequest, db: Session = Depends(get_db)):
    return TerapiasService.actualizar(id, dto.dict(), db)


# ============================================================
# PUT — CAMBIAR ESTADO (activar/desactivar)
# ============================================================
@router.put("/{id}/estado")
def cambiar_estado(id: int, db: Session = Depends(get_db)):
    TerapiasService.cambiar_estado(id, db)
    return {"mensaje": "Estado de la terapia actualizado"}


# ============================================================
# POST — ASIGNAR PERSONAL A TERAPIA
# ============================================================
@router.post("/asignar")
def asignar(dto: AsignarPersonalRequest, db: Session = Depends(get_db)):
    TerapiasService.asignar(dto.id_personal, dto.id_terapia, db)
    return {"mensaje": "Personal asignado a terapia"}
