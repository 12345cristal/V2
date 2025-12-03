# app/api/v1/endpoints/ninos.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.nino import Nino
from app.schemas.nino import NinoCreate, NinoUpdate, NinoRead

router = APIRouter(
    prefix="/ninos",
    tags=["ninos"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("/", response_model=List[NinoRead])
def list_ninos(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    tutor_id: int | None = None,
):
    query = db.query(Nino)
    if tutor_id is not None:
        query = query.filter(Nino.tutor_principal_id == tutor_id)

    ninos = (
        query.order_by(Nino.fecha_registro.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return ninos


@router.post("/", response_model=NinoRead, status_code=status.HTTP_201_CREATED)
def create_nino(
    data: NinoCreate,
    db: Session = Depends(get_db),
):
    nino = Nino(**data.model_dump())
    db.add(nino)
    db.commit()
    db.refresh(nino)
    return nino


@router.get("/{nino_id}", response_model=NinoRead)
def get_nino(
    nino_id: int,
    db: Session = Depends(get_db),
):
    nino = db.get(Nino, nino_id)
    if not nino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Niño no encontrado",
        )
    return nino


@router.put("/{nino_id}", response_model=NinoRead)
def update_nino(
    nino_id: int,
    data: NinoUpdate,
    db: Session = Depends(get_db),
):
    nino = db.get(Nino, nino_id)
    if not nino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Niño no encontrado",
        )
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(nino, field, value)
    db.commit()
    db.refresh(nino)
    return nino


@router.delete("/{nino_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nino(
    nino_id: int,
    db: Session = Depends(get_db),
):
    nino = db.get(Nino, nino_id)
    if not nino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Niño no encontrado",
        )
    db.delete(nino)
    db.commit()
    return
