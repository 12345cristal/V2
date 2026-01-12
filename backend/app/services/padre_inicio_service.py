from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import func

from models.ninos import Nino
from models.citas import Cita
from models.estado_cita import EstadoCita
from models.terapias import Terapia
from models.personal import Personal
from models.historial_progreso import HistorialProgreso
from models.ninos_archivos import NinosArchivos
from models.medicamentos import Medicamento
from models.recursos import Recurso
from models.pagos import Pago  # cuando lo tengas


def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    return hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )


def obtener_dashboard_padre(db: Session, nino_id: int):

    # =============================
    # HIJO
    # =============================
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    if not nino:
        return None

    archivos = db.query(NinosArchivos).filter_by(nino_id=nino.id).first()

    hijo = {
        "id": nino.id,
        "nombre": f"{nino.nombre} {nino.apellido_paterno}",
        "edad": calcular_edad(nino.fecha_nacimiento),
        "diagnostico": None,
        "foto_url": archivos.foto_url if archivos else None
    }

    # =============================
    # SESIONES HOY / SEMANA
    # =============================
    hoy = date.today()

    sesiones_query = (
        db.query(Cita, Terapia, Personal, EstadoCita)
        .join(Terapia, Cita.terapia_id == Terapia.id)
        .join(Personal, Cita.terapeuta_id == Personal.id)
        .join(EstadoCita, Cita.estado_id == EstadoCita.id)
        .filter(Cita.nino_id == nino.id)
    )

    sesiones_hoy = []
    sesiones_semana = []

    for cita, terapia, terapeuta, estado in sesiones_query.all():
        sesion = {
            "fecha": cita.fecha,
            "hora_inicio": cita.hora_inicio,
            "hora_fin": cita.hora_fin,
            "terapia": terapia.nombre,
            "terapeuta": f"{terapeuta.nombres} {terapeuta.apellido_paterno}",
            "estado": estado.nombre
        }

        if cita.fecha == hoy:
            sesiones_hoy.append(sesion)

        if cita.fecha >= hoy:
            sesiones_semana.append(sesion)

    # =============================
    # PROGRESO
    # =============================
    total_sesiones = db.query(func.count(HistorialProgreso.id))\
        .filter(HistorialProgreso.nino_id == nino.id)\
        .scalar() or 0

    sesiones_completadas = db.query(func.count(HistorialProgreso.id))\
        .filter(
            HistorialProgreso.nino_id == nino.id,
            HistorialProgreso.calificacion.isnot(None)
        ).scalar() or 0

    porcentaje = int((sesiones_completadas / total_sesiones) * 100) if total_sesiones > 0 else 0

    progreso = {
        "sesiones_totales": total_sesiones,
        "sesiones_completadas": sesiones_completadas,
        "porcentaje": porcentaje
    }

    # =============================
    # PAGOS (placeholder limpio)
    # =============================
    pagos = {
        "monto_total": 0.0,
        "monto_pagado": 0.0,
        "monto_pendiente": 0.0,
        "ultimo_pago_fecha": None
    }

    # =============================
    # ALERTAS
    # =============================
    alertas = {
        "documentos_nuevos": db.query(NinosArchivos).filter(NinosArchivos.nino_id == nino.id).count(),
        "medicamentos_nuevos": db.query(Medicamento).filter(
            Medicamento.nino_id == nino.id,
            Medicamento.novedadReciente == 1
        ).count(),
        "recursos_nuevos": db.query(Recurso).count()
    }

    return {
        "hijo": hijo,
        "sesiones_hoy": sesiones_hoy,
        "sesiones_semana": sesiones_semana,
        "progreso": progreso,
        "pagos": pagos,
        "alertas": alertas
    }
