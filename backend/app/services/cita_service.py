# app/services/citas_service.py
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from app.schemas.cita import CitaCreate, CitaUpdate
from app.models.cita import Cita
from app.services.notificaciones_service import crear_notificacion
from app.services.auditoria_service import registrar_accion
from app.services.ai.topsis_service import calcular_prioridad_cita


def crear_cita(db: Session, data: CitaCreate, usuario_id: int):

    hora_fin = (
        datetime.combine(datetime.today(), data.hora_inicio)
        + timedelta(minutes=data.duracionMinutos)
    ).time()

    cita = Cita(
        fecha=data.fecha,
        hora_inicio=data.hora_inicio,
        hora_fin=hora_fin,
        estado_id=data.estado_id,
        motivo=data.motivo,
        diagnostico_presuntivo=data.diagnostico_presuntivo,
        observaciones=data.observaciones,

        temp_nino_nombre=data.nombreNino,
        temp_tutor_nombre=data.tutorNombre,
        telefono_temporal=data.telefonoTutor1,
    )

    db.add(cita)
    db.commit()
    db.refresh(cita)

    registrar_accion(db, usuario_id, "crear", "citas", cita.id)

    crear_notificacion(
        db,
        usuario_id=cita.terapeuta_id,
        titulo="Nueva cita asignada",
        mensaje=f"Tienes una nueva cita el {cita.fecha}",
        tipo="cambio-horario"
    )

    return cita


def listar_citas(db: Session, fecha=None, estado=None):

    query = db.query(Cita)

    if fecha:
        query = query.filter(Cita.fecha == fecha)

    if estado:
        query = query.filter(Cita.estado_id == estado)

    return query.all()


def actualizar_cita(db: Session, id: int, data: CitaUpdate, usuario_id: int):

    cita = db.query(Cita).filter(Cita.id == id).first()

    if not cita:
        raise Exception("Cita no encontrada")

    for campo, valor in data.dict().items():
        if hasattr(cita, campo) and valor is not None:
            setattr(cita, campo, valor)

    db.commit()
    db.refresh(cita)

    registrar_accion(db, usuario_id, "actualizar", "citas", cita.id)

    return cita


def cancelar_cita(db: Session, id: int, motivo: str, usuario_id: int):
    cita = db.query(Cita).filter(Cita.id == id).first()
    if not cita:
        raise Exception("No existe la cita")

    cita.estado_id = 3  # CANCELADA
    cita.motivo = motivo

    db.commit()

    registrar_accion(db, usuario_id, "cancelar", "citas", cita.id)

    return cita
