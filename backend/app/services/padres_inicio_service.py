# services/padres_inicio_service.py
from sqlalchemy.orm import Session
from uuid import UUID

def obtener_inicio_padre(db: Session, padre_id: UUID, hijo_id: UUID | None):

    # 1️⃣ Resolver hijo (primero por defecto si no viene)
    hijo = resolver_hijo(db, padre_id, hijo_id)

    # 2️⃣ Próxima sesión
    proxima_sesion = obtener_proxima_sesion(db, hijo.id)

    # 3️⃣ Último avance
    ultimo_avance = obtener_ultimo_avance(db, hijo.id)

    # 4️⃣ Pagos
    pagos_pendientes = obtener_pagos_pendientes(db, hijo.id)

    # 5️⃣ Documento nuevo
    documento_nuevo = existen_documentos_nuevos(db, hijo.id)

    # 6️⃣ Última observación
    ultima_observacion = obtener_ultima_observacion(db, hijo.id)

    return {
        "hijo_id": hijo.id,
        "hijo_nombre": hijo.nombre,
        "proxima_sesion": proxima_sesion,
        "ultimo_avance": ultimo_avance,
        "pagos_pendientes": pagos_pendientes,
        "documento_nuevo": documento_nuevo,
        "ultima_observacion": ultima_observacion,
    }
