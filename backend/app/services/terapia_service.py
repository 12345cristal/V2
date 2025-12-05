# app/services/terapia_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.terapia import Terapia
from app.models.personal import Personal
from app.schemas.terapia import TerapiaCreate, TerapiaUpdate


def listar_terapias(db: Session):
    return db.query(Terapia).all()


def crear_terapia(db: Session, data: TerapiaCreate):
    terapia = Terapia(**data.model_dump())
    db.add(terapia)
    db.commit()
    db.refresh(terapia)
    return terapia


def actualizar_terapia(db: Session, id: int, data: TerapiaUpdate):
    terapia = db.query(Terapia).filter(Terapia.id_terapia == id).first()
    if not terapia:
        raise HTTPException(404, "Terapia no encontrada")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(terapia, key, value)

    db.commit()
    db.refresh(terapia)
    return terapia


def cambiar_estado(db: Session, id: int):
    terapia = db.query(Terapia).filter(Terapia.id_terapia == id).first()
    if not terapia:
        raise HTTPException(404, "Terapia no encontrada")

    terapia.estado = "INACTIVA" if terapia.estado == "ACTIVA" else "ACTIVA"
    db.commit()
    db.refresh(terapia)
    return terapia


def personal_sin_terapia(db: Session):
    return db.query(Personal).filter(Personal.id_terapia_principal.is_(None)).all()


def personal_con_terapia(db: Session):
    personal = db.query(Personal).all()
    result = []
    for p in personal:
        result.append({
            "id_personal": p.id_personal,
            "nombre_completo": f"{p.nombres} {p.apellido_paterno}",
            "especialidad": p.especialidad_principal,
            "id_terapia": p.id_terapia_principal
        })
    return result


def asignar_terapia(db: Session, id_personal: int, id_terapia: int):
    # validar persona
    personal = db.query(Personal).filter(Personal.id_personal == id_personal).first()
    if not personal:
        raise HTTPException(404, "Personal no encontrado")

    # validar terapia
    terapia = db.query(Terapia).filter(Terapia.id_terapia == id_terapia).first()
    if not terapia:
        raise HTTPException(404, "Terapia no encontrada")

    # Validación: SOLO 1 terapia principal
    if personal.id_terapia_principal is not None:
        raise HTTPException(
            status_code=400,
            detail="Este personal ya tiene una terapia principal asignada."
        )

    personal.id_terapia_principal = id_terapia
    db.commit()
    db.refresh(personal)
    return personal
