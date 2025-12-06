# app/services/terapia_service.py

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.terapia import Terapia, AsignacionTerapia, EstadoTerapiaEnum
from app.models.personal import Personal
from app.schemas.terapia import (
    TerapiaCreate,
    TerapiaUpdate,
    PersonalConTerapia,
    AsignacionTerapiaCreate,
)


# =============================================================
# TERAPIAS
# =============================================================
def list_terapias(db: Session) -> List[Terapia]:
    """
    Retorna todas las terapias registradas.
    """
    return db.query(Terapia).all()


def create_terapia(db: Session, obj_in: TerapiaCreate) -> Terapia:
    """
    Crea una nueva terapia asegurando que el nombre sea único.
    """
    exists = db.query(Terapia).filter(Terapia.nombre == obj_in.nombre).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una terapia con ese nombre.",
        )
    terapia = Terapia(
        nombre=obj_in.nombre,
        descripcion=obj_in.descripcion,
        estado=EstadoTerapiaEnum.ACTIVA,
    )
    db.add(terapia)
    db.commit()
    db.refresh(terapia)
    return terapia


def get_terapia(db: Session, id_terapia: int) -> Terapia:
    """
    Obtiene una terapia por su ID.
    """
    terapia = db.query(Terapia).get(id_terapia)
    if not terapia:
        raise HTTPException(status_code=404, detail="Terapia no encontrada")
    return terapia


def update_terapia(db: Session, id_terapia: int, obj_in: TerapiaUpdate) -> Terapia:
    """
    Actualiza los campos proporcionados de una terapia existente.
    """
    terapia = get_terapia(db, id_terapia)
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(terapia, field, value)
    db.add(terapia)
    db.commit()
    db.refresh(terapia)
    return terapia


def toggle_estado_terapia(db: Session, id_terapia: int) -> Terapia:
    """
    Cambia el estado de la terapia entre ACTIVA e INACTIVA.
    """
    terapia = get_terapia(db, id_terapia)
    terapia.estado = (
        EstadoTerapiaEnum.INACTIVA
        if terapia.estado == EstadoTerapiaEnum.ACTIVA
        else EstadoTerapiaEnum.ACTIVA
    )
    db.add(terapia)
    db.commit()
    db.refresh(terapia)
    return terapia


# =============================================================
# PERSONAL Y SUS TERAPIAS
# =============================================================
def get_personal_sin_terapia(db: Session) -> List[Personal]:
    """
    Obtiene el personal que no tiene terapia principal asignada.
    """
    return db.query(Personal).filter(Personal.id_terapia_principal.is_(None)).all()


def get_personal_asignado(db: Session) -> List[PersonalConTerapia]:
    """
    Obtiene el personal junto con su terapia asignada.
    Incluye personal sin terapia mediante outer join.
    """
    query = (
        db.query(
            Personal.id_personal,
            (Personal.nombres + " " + Personal.apellido_paterno + " " + (Personal.apellido_materno or "")).label("nombre_completo"),
            Personal.especialidad_principal.label("especialidad"),
            Terapia.id_terapia,
            Terapia.nombre.label("nombre_terapia"),
        )
        .outerjoin(Terapia, Personal.id_terapia_principal == Terapia.id_terapia)
    )

    resultados = [
        PersonalConTerapia(
            id_personal=row.id_personal,
            nombre_completo=row.nombre_completo.strip(),
            especialidad=row.especialidad,
            id_terapia=row.id_terapia,
            nombre_terapia=row.nombre_terapia,
        )
        for row in query.all()
    ]
    return resultados


# =============================================================
# ASIGNACIÓN DE TERAPIAS
# =============================================================
def asignar_terapia_a_personal(
    db: Session, data: AsignacionTerapiaCreate
) -> AsignacionTerapia:
    """
    Asigna una terapia a un miembro del personal.

    Pasos:
    1. Valida que el personal exista.
    2. Valida que la terapia exista.
    3. Asegura que el personal no tenga otra terapia principal.
    4. Actualiza el campo `id_terapia_principal` en la tabla Personal.
    5. Crea un registro en la tabla AsignacionTerapia si no existe previamente.
    """
    personal = db.query(Personal).get(data.id_personal)
    if not personal:
        raise HTTPException(status_code=404, detail="Personal no encontrado")

    terapia = db.query(Terapia).get(data.id_terapia)
    if not terapia:
        raise HTTPException(status_code=404, detail="Terapia no encontrada")

    # Validación: solo una terapia principal
    if personal.id_terapia_principal and personal.id_terapia_principal != terapia.id_terapia:
        raise HTTPException(
            status_code=400,
            detail="La persona ya tiene una terapia principal asignada.",
        )

    # Actualizar campo en Personal
    personal.id_terapia_principal = terapia.id_terapia
    db.add(personal)

    # Registrar en AsignacionTerapia si no existe
    asignacion = (
        db.query(AsignacionTerapia)
        .filter(
            AsignacionTerapia.id_personal == data.id_personal,
            AsignacionTerapia.id_terapia == data.id_terapia,
        )
        .first()
    )
    if not asignacion:
        asignacion = AsignacionTerapia(
            id_personal=data.id_personal,
            id_terapia=data.id_terapia,
            es_principal=True,
        )
        db.add(asignacion)

    db.commit()
    db.refresh(asignacion)
    return asignacion
