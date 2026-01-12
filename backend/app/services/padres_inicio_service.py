from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import UUID
from datetime import datetime, timedelta

from models.nino import Nino
from models.terapia import TerapiaNino
from models.avance import Avance
from models.observacion import Observacion
from models.pago import Pago
from schemas.padres_inicio import (
    InicioPadreResponse,
    HijoResumen,
    ProximaSesionSchema,
    UltimoAvanceSchema,
    UltimaObservacionSchema
)

def obtener_inicio_padre(db: Session, tutor_id: UUID, hijo_id: UUID | None = None) -> InicioPadreResponse:

    if hijo_id:
        hijo = db.query(Nino).filter(
            and_(Nino.id == hijo_id, Nino.tutor_id == tutor_id, Nino.activo == True)
        ).first()
    else:
        hijo = db.query(Nino).filter(
            and_(Nino.tutor_id == tutor_id, Nino.activo == True)
        ).order_by(Nino.fecha_creacion.desc()).first()

    hijos_activos = db.query(Nino).filter(
        and_(Nino.tutor_id == tutor_id, Nino.activo == True)
    ).all()

    proxima_sesion = db.query(TerapiaNino).filter(
        and_(TerapiaNino.nino_id == hijo.id, TerapiaNino.fecha >= datetime.now())
    ).order_by(TerapiaNino.fecha.asc()).first()

    ultimo_avance = db.query(Avance).filter(
        Avance.nino_id == hijo.id
    ).order_by(Avance.fecha.desc()).first()

    ultima_observacion = db.query(Observacion).filter(
        Observacion.nino_id == hijo.id
    ).order_by(Observacion.fecha.desc()).first()

    pagos_pendientes = db.query(Pago).filter(
        and_(Pago.nino_id == hijo.id, Pago.estado == 'pendiente')
    ).count()

    documentos_nuevos = db.query(Observacion).filter(
        and_(Observacion.nino_id == hijo.id, Observacion.fecha >= datetime.now() - timedelta(days=7))
    ).count()

    porcentaje_progreso = ultimo_avance.porcentaje if ultimo_avance else 0

    return InicioPadreResponse(
        hijoSeleccionado=HijoResumen(
            id=str(hijo.id),
            nombre=hijo.nombre,
            edad=calcular_edad(hijo.fecha_nacimiento),
            fotoPerfil=hijo.foto_url,
            estado='activo'
        ),
        hijosActivos=[
            HijoResumen(
                id=str(h.id),
                nombre=h.nombre,
                edad=calcular_edad(h.fecha_nacimiento),
                fotoPerfil=h.foto_url,
                estado='activo'
            ) for h in hijos_activos
        ],
        proximaSesion=ProximaSesionSchema(
            id=str(proxima_sesion.id),
            fecha=proxima_sesion.fecha.isoformat(),
            hora=proxima_sesion.fecha.strftime("%H:%M"),
            tipo=proxima_sesion.tipo_terapia,
            terapeuta=proxima_sesion.terapeuta.nombre,
            estado='pendiente'
        ) if proxima_sesion else None,
        ultimoAvance=UltimoAvanceSchema(
            id=str(ultimo_avance.id),
            fecha=ultimo_avance.fecha.isoformat(),
            descripcion=ultimo_avance.descripcion,
            porcentaje=ultimo_avance.porcentaje,
            area=ultimo_avance.area
        ) if ultimo_avance else None,
        pagosPendientes=pagos_pendientes,
        documentosNuevos=documentos_nuevos,
        ultimaObservacion=UltimaObservacionSchema(
            id=str(ultima_observacion.id),
            fecha=ultima_observacion.fecha.isoformat(),
            terapeuta=ultima_observacion.terapeuta.nombre,
            resumen=ultima_observacion.resumen
        ) if ultima_observacion else None,
        porcentajeProgreso=porcentaje_progreso
    )

def calcular_edad(fecha_nacimiento: datetime) -> int:
    hoy = datetime.now()
    edad = hoy.year - fecha_nacimiento.year
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad
