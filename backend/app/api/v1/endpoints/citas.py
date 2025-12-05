# app/api/v1/endpoints/citas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_role
from app.schemas.cita import CitaCreate, CitaUpdate
from app.services.citas_service import (
    crear_cita, actualizar_cita, listar_citas, cancelar_cita
)

router = APIRouter(prefix="/citas", tags=["Citas"])


@router.get("/", dependencies=[Depends(require_role(2))])
def obtener_citas(
    fecha: str | None = None,
    estado: int | None = None,
    db: Session = Depends(get_db)
):
    return listar_citas(db, fecha, estado)


@router.post("/", dependencies=[Depends(require_role(2))])
def crear(data: CitaCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crear_cita(db, data, user.id)


@router.put("/{id}", dependencies=[Depends(require_role(2))])
def actualizar(id: int, data: CitaUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return actualizar_cita(db, id, data, user.id)


@router.post("/{id}/cancelar", dependencies=[Depends(require_role(2))])
def cancelar(id: int, motivo: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return cancelar_cita(db, id, motivo, user.id)
