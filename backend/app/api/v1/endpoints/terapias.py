from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permissions
from app.models.terapia import Terapia
from app.models.personal_terapia import PersonalTerapia
from app.models.personal import Personal
from app.schemas.terapia import (
    TerapiaCreate, TerapiaRead, TerapiaUpdate, PersonalAsignado
)

router = APIRouter(
    prefix="/terapias",
    tags=["terapias"],
    dependencies=[Depends(require_permissions(["terapias:ver"]))]
)


# ===============================
# LISTAR TODAS LAS TERAPIAS
# ===============================
@router.get("/", response_model=list[TerapiaRead])
def list_terapias(db: Session = Depends(get_db)):
    return db.query(Terapia).order_by(Terapia.nombre).all()


# ===============================
# CREAR TERAPIA
# ===============================
@router.post("/", response_model=TerapiaRead,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_permissions(["terapias:crear"]))])
def create_terapia(data: TerapiaCreate, db: Session = Depends(get_db)):
    terapia = Terapia(**data.model_dump())
    db.add(terapia)
    db.commit()
    db.refresh(terapia)
    return terapia


# ===============================
# OBTENER TERAPIA
# ===============================
@router.get("/{terapia_id}", response_model=TerapiaRead)
def get_terapia(terapia_id: int, db: Session = Depends(get_db)):
    terapia = db.get(Terapia, terapia_id)
    if not terapia:
        raise HTTPException(404, "Terapia no encontrada")
    return terapia


# ===============================
# ACTUALIZAR TERAPIA
# ===============================
@router.put("/{terapia_id}", response_model=TerapiaRead,
            dependencies=[Depends(require_permissions(["terapias:editar"]))])
def update_terapia(terapia_id: int, data: TerapiaUpdate, db: Session = Depends(get_db)):
    terapia = db.get(Terapia, terapia_id)
    if not terapia:
        raise HTTPException(404, "Terapia no encontrada")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(terapia, k, v)

    db.commit()
    db.refresh(terapia)
    return terapia


# ===============================
# ELIMINAR TERAPIA
# ===============================
@router.delete("/{terapia_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_permissions(["terapias:eliminar"]))])
def delete_terapia(terapia_id: int, db: Session = Depends(get_db)):
    terapia = db.get(Terapia, terapia_id)
    if not terapia:
        raise HTTPException(404, "Terapia no encontrada")

    db.delete(terapia)
    db.commit()
    return


# ===============================
# LISTAR PERSONAL ASIGNADO A UNA TERAPIA
# ===============================
@router.get("/{terapia_id}/personal", response_model=list[PersonalAsignado])
def list_personal_asignado(terapia_id: int, db: Session = Depends(get_db)):
    asignaciones = (
        db.query(PersonalTerapia)
        .filter(PersonalTerapia.terapia_id == terapia_id)
        .all()
    )

    result = []
    for a in asignaciones:
        nombre = (
            f"{a.personal.usuario.nombres} "
            f"{a.personal.usuario.apellido_paterno} "
            f"{a.personal.usuario.apellido_materno or ''}".strip()
        )

        result.append(PersonalAsignado(
            id=a.id,
            personal_id=a.personal_id,
            nombre_completo=nombre
        ))

    return result


# ===============================
# ASIGNAR TERAPEUTA A TERAPIA
# ===============================
@router.post("/{terapia_id}/asignar/{personal_id}",
             response_model=PersonalAsignado,
             dependencies=[Depends(require_permissions(["terapias:asignar"]))]
)
def asignar_personal(terapia_id: int, personal_id: int, db: Session = Depends(get_db)):

    # validar existencia
    terapia = db.get(Terapia, terapia_id)
    personal = db.get(Personal, personal_id)

    if not terapia: raise HTTPException(404, "Terapia no encontrada")
    if not personal: raise HTTPException(404, "Personal no encontrado")

    # evitar duplicados
    exists = db.query(PersonalTerapia).filter_by(
        terapia_id=terapia_id,
        personal_id=personal_id
    ).first()

    if exists:
        raise HTTPException(400, "El terapeuta ya está asignado a esta terapia")

    relacion = PersonalTerapia(
        terapia_id=terapia_id,
        personal_id=personal_id
    )
    db.add(relacion)
    db.commit()
    db.refresh(relacion)

    nombre = (
        f"{personal.usuario.nombres} "
        f"{personal.usuario.apellido_paterno} "
        f"{personal.usuario.apellido_materno or ''}".strip()
    )

    return PersonalAsignado(
        id=relacion.id,
        personal_id=personal_id,
        nombre_completo=nombre
    )


# ===============================
# DESASIGNAR TERAPEUTA
# ===============================
@router.delete(
    "/{terapia_id}/desasignar/{asignacion_id}",
    status_code=204,
    dependencies=[Depends(require_permissions(["terapias:asignar"]))]
)
def remove_personal(terapia_id: int, asignacion_id: int, db: Session = Depends(get_db)):
    relacion = db.get(PersonalTerapia, asignacion_id)
    if not relacion or relacion.terapia_id != terapia_id:
        raise HTTPException(404, "Asignación no encontrada")

    db.delete(relacion)
    db.commit()
