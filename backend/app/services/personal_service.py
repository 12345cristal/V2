# app/services/personal_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.models.personal import Personal, HorarioPersonal
from app.schemas.personal import (
    PersonalCreate, PersonalUpdate, PersonalRead, HorarioPersonalBase
)


def crear_personal(db: Session, data: PersonalCreate) -> Personal:
    personal = Personal(
        **data.model_dump(exclude={"horarios"})
    )
    db.add(personal)
    db.flush()

    if data.horarios:
        for h in data.horarios:
            horario = HorarioPersonal(
                id_personal=personal.id_personal,
                dia_semana=h.dia_semana,
                hora_inicio=h.hora_inicio,
                hora_fin=h.hora_fin,
            )
            db.add(horario)

    db.commit()
    db.refresh(personal)
    return personal


def listar_personal(db: Session) -> List[Personal]:
    return db.query(Personal).all()


def obtener_personal(db: Session, id_personal: int) -> Personal:
    personal = db.query(Personal).get(id_personal)
    if not personal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal no encontrado"
        )
    return personal


def actualizar_personal(
    db: Session,
    id_personal: int,
    data: PersonalUpdate
) -> Personal:
    personal = obtener_personal(db, id_personal)
    for key, value in data.model_dump(exclude_unset=True).items():
        if key == "horarios" and value is not None:
            # reemplazar horarios
            personal.horarios.clear()
            for h in value:
                horario = HorarioPersonal(
                    id_personal=personal.id_personal,
                    dia_semana=h["dia_semana"],
                    hora_inicio=h["hora_inicio"],
                    hora_fin=h["hora_fin"],
                )
                db.add(horario)
        else:
            setattr(personal, key, value)

    db.commit()
    db.refresh(personal)
    return personal


def eliminar_personal(db: Session, id_personal: int) -> None:
    personal = obtener_personal(db, id_personal)
    db.delete(personal)
    db.commit()
