# app/api/v1/endpoints/terapias.py

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_permissions
from app.schemas.terapia import (
    TerapiaRead,
    TerapiaCreate,
    TerapiaUpdate,
    PersonalConTerapia,
    AsignacionTerapiaCreate,
)
from app.services.terapia_service import (
    list_terapias,
    create_terapia,
    update_terapia,
    toggle_estado_terapia,
    get_personal_sin_terapia,
    get_personal_asignado,
    asignar_terapia_a_personal,
)

router = APIRouter(
    prefix="/terapias",
    tags=["Terapias"],
    dependencies=[Depends(get_current_active_user)]
)

# =============================================================
# CRUD TERAPIAS
# =============================================================

@router.get("", response_model=List[TerapiaRead])
def listar_terapias_endpoint(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["TERAPIAS_VER"]))
):
    """
    Listado de todas las terapias.
    Requiere permiso: TERAPIAS_VER
    """
    return list_terapias(db)


@router.post("", response_model=TerapiaRead, status_code=status.HTTP_201_CREATED)
def crear_terapia_endpoint(
    obj_in: TerapiaCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["TERAPIAS_CREAR"]))
):
    """
    Crear una nueva terapia.
    Requiere permiso: TERAPIAS_CREAR
    """
    return create_terapia(db, obj_in)


@router.put("/{id_terapia}", response_model=TerapiaRead)
def actualizar_terapia_endpoint(
    id_terapia: int,
    obj_in: TerapiaUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["TERAPIAS_EDITAR"]))
):
    """
    Actualiza los datos de una terapia existente.
    Requiere permiso: TERAPIAS_EDITAR
    """
    return update_terapia(db, id_terapia, obj_in)


@router.patch("/{id_terapia}/estado", response_model=TerapiaRead)
def cambiar_estado_terapia_endpoint(
    id_terapia: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["TERAPIAS_EDITAR"]))
):
    """
    Cambia el estado de la terapia (ACTIVA <-> INACTIVA).
    Requiere permiso: TERAPIAS_EDITAR
    """
    return toggle_estado_terapia(db, id_terapia)


# =============================================================
# PERSONAL Y SUS TERAPIAS
# =============================================================

@router.get("/personal-asignado", response_model=List[PersonalConTerapia])
def listar_personal_asignado_endpoint(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["TERAPIAS_VER"]))
):
    """
    Listado de personal junto con su terapia asignada.
    Requiere permiso: TERAPIAS_VER
    """
    return get_personal_asignado(db)


@router.get("/personal/sin-terapia", response_model=List[PersonalConTerapia])
def listar_personal_sin_terapia_endpoint(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["TERAPIAS_VER"]))
):
    """
    Listado de personal que no tiene terapia principal asignada.
    Requiere permiso: TERAPIAS_VER
    """
    personal = get_personal_sin_terapia(db)
    return [
        PersonalConTerapia(
            id_personal=p.id_personal,
            nombre_completo=f"{p.nombres} {p.apellido_paterno} {p.apellido_materno or ''}".strip(),
            especialidad=p.especialidad_principal,
            id_terapia=None,
            nombre_terapia=None,
        )
        for p in personal
    ]


# =============================================================
# ASIGNACIÓN DE TERAPIAS
# =============================================================

@router.post("/asignar", status_code=status.HTTP_201_CREATED, response_model=PersonalConTerapia)
def asignar_terapia_endpoint(
    obj_in: AsignacionTerapiaCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["TERAPIAS_ASIGNAR"]))
):
    """
    Asigna una terapia a un miembro del personal.
    Actualiza `id_terapia_principal` y registra en tabla intermedia.
    Requiere permiso: TERAPIAS_ASIGNAR
    """
    asignacion = asignar_terapia_a_personal(db, obj_in)

    return PersonalConTerapia(
        id_personal=asignacion.id_personal,
        nombre_completo=f"{asignacion.personal.nombres} {asignacion.personal.apellido_paterno} {asignacion.personal.apellido_materno or ''}".strip(),
        especialidad=asignacion.personal.especialidad_principal,
        id_terapia=asignacion.id_terapia,
        nombre_terapia=asignacion.terapia.nombre,
    )
