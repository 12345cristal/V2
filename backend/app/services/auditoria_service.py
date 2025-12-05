# app/services/auditoria_service.py

from sqlalchemy.orm import Session
from app.models.auditoria import Auditoria
from datetime import datetime


def registrar_evento(db: Session, usuario_id: int | None, accion: str, tabla_afectada: str, registro_id: int | None):
    evento = Auditoria(
        usuario_id=usuario_id,
        accion=accion,
        tabla_afectada=tabla_afectada,
        registro_id=registro_id,
        fecha=datetime.now()
    )
    db.add(evento)
    db.commit()
