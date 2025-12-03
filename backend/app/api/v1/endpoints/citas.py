# app/api/v1/endpoints/citas.py
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.api.deps import get_db, require_permissions
from app.models.cita import Cita, CitaObservador
from app.models.catalogos import CatEstadoCita
from app.models.personal import Personal
from app.models.nino import Nino
from app.models.terapia import Terapia
from app.schemas.cita import (
    CitaCreate, CitaRead, CitaUpdate, CitaObservadorRead
)

router = APIRouter(
    prefix="/citas",
    tags=["citas"],
    dependencies=[Depends(require_permissions(["citas:ver"]))]
)


# ===============================
# Helper: obtener estado por código
# ===============================
def get_estado_id(db: Session, codigo: str) -> int:
    estado = db.query(CatEstadoCita).filter(CatEstadoCita.codigo == codigo).first()
    if not estado:
        raise HTTPException(
            status_code=500,
            detail=f"No está configurado el estado de cita '{codigo}' en cat_estado_cita."
        )
    return estado.id


# ===============================
# Helper: validar traslape de horarios
# ===============================
def validar_traslape_citas(
    db: Session,
    terapeuta_id: int | None,
    fecha: date,
    hora_inicio,
    hora_fin,
    cita_id_excluir: int | None = None,
):
    if terapeuta_id is None:
        return

    query = db.query(Cita).filter(
        Cita.terapeuta_id == terapeuta_id,
        Cita.fecha == fecha,
        # traslape: (inicio < fin_nueva) y (fin > inicio_nueva)
        Cita.hora_inicio < hora_fin,
        Cita.hora_fin > hora_inicio,
    )

    if cita_id_excluir is not None:
        query = query.filter(Cita.id != cita_id_excluir)

    if query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El terapeuta ya tiene una cita en ese horario."
        )


# ===============================
# Helper: construir CitaRead
# ===============================
def build_cita_read(cita: Cita) -> CitaRead:
    # nombre del niño (si existe) o temporal
    if cita.nino:
        nombre_mostrado = (
            f"{cita.nino.nombre} {cita.nino.apellido_paterno} "
            f"{cita.nino.apellido_materno or ''}".strip()
        )
    else:
        nombre_mostrado = (
            f"{cita.temp_nino_nombre or ''} "
            f"{cita.temp_nino_apellido_paterno or ''} "
            f"{cita.temp_nino_apellido_materno or ''}"
        ).strip() or "Niño nuevo"

    terapeuta_nombre = None
    if cita.terapeuta and cita.terapeuta.usuario:
        terapeuta_nombre = (
            f"{cita.terapeuta.usuario.nombres} "
            f"{cita.terapeuta.usuario.apellido_paterno} "
            f"{cita.terapeuta.usuario.apellido_materno or ''}".strip()
        )

    terapia_nombre = cita.terapia.nombre if cita.terapia else None

    return CitaRead(
        id=cita.id,
        fecha=cita.fecha,
        hora_inicio=cita.hora_inicio,
        hora_fin=cita.hora_fin,
        nino_id=cita.nino_id,
        es_nuevo_nino=cita.es_nuevo_nino,
        nombre_mostrado=nombre_mostrado,
        terapeuta_id=cita.terapeuta_id,
        terapeuta_nombre=terapeuta_nombre,
        terapia_id=cita.terapia_id,
        terapia_nombre=terapia_nombre,
        estado_id=cita.estado_id,
        estado_codigo=cita.estado.codigo if cita.estado else "",
        estado_nombre=cita.estado.nombre if cita.estado else "",
        es_reposicion=cita.es_reposicion,
        motivo=cita.motivo,
        diagnostico_presuntivo=cita.diagnostico_presuntivo,
        observaciones=cita.observaciones,
    )


# ===============================
# LISTAR CITAS (filtros por rango, terapeuta, niño)
# ===============================
@router.get("/", response_model=List[CitaRead])
def list_citas(
    db: Session = Depends(get_db),
    fecha_desde: date | None = Query(None),
    fecha_hasta: date | None = Query(None),
    terapeuta_id: int | None = Query(None),
    nino_id: int | None = Query(None),
):
    query = db.query(Cita).join(Cita.estado)

    if fecha_desde:
        query = query.filter(Cita.fecha >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Cita.fecha <= fecha_hasta)
    if terapeuta_id:
        query = query.filter(Cita.terapeuta_id == terapeuta_id)
    if nino_id:
        query = query.filter(Cita.nino_id == nino_id)

    citas = query.order_by(Cita.fecha, Cita.hora_inicio).all()
    return [build_cita_read(c) for c in citas]


# ===============================
# OBTENER CITA POR ID
# ===============================
@router.get("/{cita_id}", response_model=CitaRead)
def get_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = db.get(Cita, cita_id)
    if not cita:
        raise HTTPException(404, "Cita no encontrada")
    return build_cita_read(cita)


# ===============================
# CREAR CITA
# ===============================
@router.post(
    "/",
    response_model=CitaRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions(["citas:crear"]))]
)
def create_cita(data: CitaCreate, db: Session = Depends(get_db)):
    # Estado por defecto: AGENDADA
    if data.estado_id is None:
        estado_id = get_estado_id(db, "AGENDADA")
    else:
        estado_id = data.estado_id

    # Validar traslape de horarios para el terapeuta
    validar_traslape_citas(
        db=db,
        terapeuta_id=data.terapeuta_id,
        fecha=data.fecha,
        hora_inicio=data.hora_inicio,
        hora_fin=data.hora_fin,
    )

    cita = Cita(
        nino_id=data.nino_id,
        es_nuevo_nino=data.es_nuevo_nino,
        temp_nino_nombre=data.temp_nino_nombre,
        temp_nino_apellido_paterno=data.temp_nino_apellido_paterno,
        temp_nino_apellido_materno=data.temp_nino_apellido_materno,
        temp_tutor_nombre=data.temp_tutor_nombre,
        temp_tutor_apellido_paterno=data.temp_tutor_apellido_paterno,
        temp_tutor_apellido_materno=data.temp_tutor_apellido_materno,
        telefono_temporal=data.telefono_temporal,
        terapeuta_id=data.terapeuta_id,
        terapia_id=data.terapia_id,
        fecha=data.fecha,
        hora_inicio=data.hora_inicio,
        hora_fin=data.hora_fin,
        estado_id=estado_id,
        es_reposicion=data.es_reposicion,
        motivo=data.motivo,
        diagnostico_presuntivo=data.diagnostico_presuntivo,
        observaciones=data.observaciones,
    )

    db.add(cita)
    db.commit()
    db.refresh(cita)

    return build_cita_read(cita)


# ===============================
# ACTUALIZAR CITA
# ===============================
@router.put(
    "/{cita_id}",
    response_model=CitaRead,
    dependencies=[Depends(require_permissions(["citas:editar"]))]
)
def update_cita(
    cita_id: int,
    data: CitaUpdate,
    db: Session = Depends(get_db),
):
    cita = db.get(Cita, cita_id)
    if not cita:
        raise HTTPException(404, "Cita no encontrada")

    payload = data.model_dump(exclude_unset=True)

    # Si se cambia fecha/hora/terapeuta => revalidar traslape
    nueva_fecha = payload.get("fecha", cita.fecha)
    nueva_inicio = payload.get("hora_inicio", cita.hora_inicio)
    nueva_fin = payload.get("hora_fin", cita.hora_fin)
    nuevo_terapeuta = payload.get("terapeuta_id", cita.terapeuta_id)

    validar_traslape_citas(
        db=db,
        terapeuta_id=nuevo_terapeuta,
        fecha=nueva_fecha,
        hora_inicio=nueva_inicio,
        hora_fin=nueva_fin,
        cita_id_excluir=cita.id,
    )

    for field, value in payload.items():
        setattr(cita, field, value)

    db.commit()
    db.refresh(cita)
    return build_cita_read(cita)


# ===============================
# CANCELAR CITA (estado = CANCELADA)
# ===============================
@router.post(
    "/{cita_id}/cancelar",
    response_model=CitaRead,
    dependencies=[Depends(require_permissions(["citas:cancelar"]))]
)
def cancelar_cita(
    cita_id: int,
    motivo: str | None = None,
    db: Session = Depends(get_db),
):
    cita = db.get(Cita, cita_id)
    if not cita:
        raise HTTPException(404, "Cita no encontrada")

    estado_cancelada_id = get_estado_id(db, "CANCELADA")
    cita.estado_id = estado_cancelada_id

    if motivo:
        # Append el motivo de cancelación a las observaciones
        if cita.observaciones:
            cita.observaciones += f"\n\n[Cancelación]: {motivo}"
        else:
            cita.observaciones = f"[Cancelación]: {motivo}"

    db.commit()
    db.refresh(cita)
    return build_cita_read(cita)


# ===============================
# ELIMINAR CITA (hard delete)
# ===============================
@router.delete(
    "/{cita_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions(["citas:eliminar"]))]
)
def delete_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = db.get(Cita, cita_id)
    if not cita:
        raise HTTPException(404, "Cita no encontrada")

    db.delete(cita)
    db.commit()
    return


# ===============================
# OBSERVADORES DE CITA
# ===============================
@router.get(
    "/{cita_id}/observadores",
    response_model=List[CitaObservadorRead]
)
def list_observadores(cita_id: int, db: Session = Depends(get_db)):
    cita = db.get(Cita, cita_id)
    if not cita:
        raise HTTPException(404, "Cita no encontrada")

    result: list[CitaObservadorRead] = []
    for obs in cita.observadores:
        nombre = None
        if obs.terapeuta and obs.terapeuta.usuario:
            nombre = (
                f"{obs.terapeuta.usuario.nombres} "
                f"{obs.terapeuta.usuario.apellido_paterno} "
                f"{obs.terapeuta.usuario.apellido_materno or ''}".strip()
            )

        result.append(CitaObservadorRead(
            id=obs.id,
            terapeuta_id=obs.terapeuta_id,
            terapeuta_nombre=nombre or "Terapeuta",
        ))
    return result


@router.post(
    "/{cita_id}/observadores/{terapeuta_id}",
    response_model=CitaObservadorRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions(["citas:editar"]))]
)
def add_observador(
    cita_id: int,
    terapeuta_id: int,
    db: Session = Depends(get_db),
):
    cita = db.get(Cita, cita_id)
    if not cita:
        raise HTTPException(404, "Cita no encontrada")

    personal = db.get(Personal, terapeuta_id)
    if not personal:
        raise HTTPException(404, "Terapeuta no encontrado")

    # evitar duplicados
    existing = db.query(CitaObservador).filter_by(
        cita_id=cita_id,
        terapeuta_id=terapeuta_id,
    ).first()

    if existing:
        raise HTTPException(400, "Ya está marcado como observador de esta cita")

    obs = CitaObservador(
        cita_id=cita_id,
        terapeuta_id=terapeuta_id,
    )
    db.add(obs)
    db.commit()
    db.refresh(obs)

    nombre = (
        f"{personal.usuario.nombres} "
        f"{personal.usuario.apellido_paterno} "
        f"{personal.usuario.apellido_materno or ''}".strip()
    )

    return CitaObservadorRead(
        id=obs.id,
        terapeuta_id=terapeuta_id,
        terapeuta_nombre=nombre,
    )


@router.delete(
    "/{cita_id}/observadores/{obs_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions(["citas:editar"]))]
)
def delete_observador(
    cita_id: int,
    obs_id: int,
    db: Session = Depends(get_db),
):
    obs = db.get(CitaObservador, obs_id)
    if not obs or obs.cita_id != cita_id:
        raise HTTPException(404, "Observador no encontrado")

    db.delete(obs)
    db.commit()
    return
