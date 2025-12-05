# app/api/v1/endpoints/terapias.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, require_permissions
from app.schemas.terapia import (
    TerapiaRead, TerapiaCreate, TerapiaUpdate, PersonalConTerapia
)
from app.services.terapia_service import (
    listar_terapias, crear_terapia, actualizar_terapia,
    cambiar_estado, personal_sin_terapia, personal_con_terapia,
    asignar_terapia
)

router = APIRouter(prefix="/terapias", tags=["Terapias"])


# ======================================================
# GET /terapias
# ======================================================
@router.get("", response_model=List[TerapiaRead])
def get_terapias(db: Session = Depends(get_db)):
    return listar_terapias(db)


# ======================================================
# POST /terapias
# ======================================================
@router.post("", response_model=TerapiaRead)
def post_terapia(data: TerapiaCreate, db: Session = Depends(get_db)):
    return crear_terapia(db, data)


# ======================================================
# PUT /terapias/{id}
# ======================================================
@router.put("/{id}", response_model=TerapiaRead)
def put_terapia(id: int, data: TerapiaUpdate, db: Session = Depends(get_db)):
    return actualizar_terapia(db, id, data)


# ======================================================
# PATCH /terapias/{id}/estado
# ======================================================
@router.patch("/{id}/estado", response_model=TerapiaRead)
def patch_cambiar_estado(id: int, db: Session = Depends(get_db)):
    return cambiar_estado(db, id)


# ======================================================
# GET /personal/sin-terapia
# ======================================================
@router.get("/personal/sin-terapia", response_model=List[PersonalConTerapia])
def get_personal_sin_terapia(db: Session = Depends(get_db)):
    lista = personal_sin_terapia(db)
    return [
        PersonalConTerapia(
            id_personal=p.id_personal,
            nombre_completo=f"{p.nombres} {p.apellido_paterno}",
            especialidad=p.especialidad_principal,
            id_terapia=None
        )
        for p in lista
    ]


# ======================================================
# GET /terapias/personal-asignado
# ======================================================
@router.get("/personal-asignado", response_model=List[PersonalConTerapia])
def get_personal_asignado(db: Session = Depends(get_db)):
    return personal_con_terapia(db)


# ======================================================
# POST /terapias/asignar
# ======================================================
@router.post("/asignar", response_model=PersonalConTerapia)
def post_asignar_terapia(
    payload: dict,
    db: Session = Depends(get_db)
):
    id_personal = payload.get("id_personal")
    id_terapia = payload.get("id_terapia")

    p = asignar_terapia(db, id_personal, id_terapia)

    return PersonalConTerapia(
        id_personal=p.id_personal,
        nombre_completo=f"{p.nombres} {p.apellido_paterno}",
        especialidad=p.especialidad_principal,
        id_terapia=p.id_terapia_principal
    )
