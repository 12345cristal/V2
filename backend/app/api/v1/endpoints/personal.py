# app/api/v1/endpoints/personal.py
from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import List, Optional
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_permissions
from app.schemas.personal import PersonalCreate, PersonalUpdate, PersonalRead
from app.models.rol import Rol
from app.services.personal_service import (
    crear_personal,
    listar_personal,
    obtener_personal,
    actualizar_personal,
    eliminar_personal,
)

router = APIRouter(
    prefix="/personal",
    tags=["personal"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/roles", response_model=List[RolRead])  # define RolRead en schemas
def get_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()


@router.get("/personal", response_model=List[PersonalRead])
def get_personal(
    db: Session = Depends(get_db),
    _=Depends(require_permissions(["PERSONAL_VER"]))
):
    return listar_personal(db)


@router.get("/personal/{id_personal}", response_model=PersonalRead)
def get_personal_by_id(
    id_personal: int,
    db: Session = Depends(get_db),
    _=Depends(require_permissions(["PERSONAL_VER"]))
):
    return obtener_personal(db, id_personal)


@router.post("/personal", response_model=PersonalRead)
def create_personal(
    data: PersonalCreate,
    db: Session = Depends(get_db),
    _=Depends(require_permissions(["PERSONAL_CREAR"]))
):
    return crear_personal(db, data)


@router.put("/personal/{id_personal}", response_model=PersonalRead)
def update_personal(
    id_personal: int,
    data: PersonalUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_permissions(["PERSONAL_EDITAR"]))
):
    return actualizar_personal(db, id_personal, data)


@router.delete("/personal/{id_personal}")
def delete_personal(
    id_personal: int,
    db: Session = Depends(get_db),
    _=Depends(require_permissions(["PERSONAL_ELIMINAR"]))
):
    eliminar_personal(db, id_personal)
    return {"ok": True}
