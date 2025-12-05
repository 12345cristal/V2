# app/utils/auditoria.py
from typing import Optional
from sqlalchemy.orm import Session

from app.models.auditoria import Auditoria


def registrar_auditoria(
    db: Session,
    usuario_id: Optional[int],
    accion: str,
    tabla_afectada: str,
    registro_id: Optional[int],
) -> None:
    """
    Registra una acción en la tabla auditoria.
    Debe llamarse desde los servicios al crear/actualizar/eliminar.
    """
    entry = Auditoria(
        usuario_id=usuario_id,
        accion=accion,
        tabla_afectada=tabla_afectada,
        registro_id=registro_id,
    )
    db.add(entry)
    # Commit NO se hace aquí, se delega al servicio que la llama
