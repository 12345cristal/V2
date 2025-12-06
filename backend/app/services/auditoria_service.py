# app/services/auditoria_service.py

from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.auditoria import Auditoria


def registrar_evento(
    db: Session,
    *,
    usuario_id: Optional[int] = None,
    usuario_nombre: Optional[str] = None,
    rol_usuario: Optional[str] = None,
    modulo: str,
    accion: str,
    descripcion: Optional[str] = None,
    detalle: Optional[Dict] = None,
    ip: Optional[str] = None,
) -> None:
    """
    Registra un evento en la tabla de auditoría.
    """
    evento = Auditoria(
        fecha_hora=datetime.utcnow(),
        usuario_id=usuario_id,
        usuario_nombre=usuario_nombre,
        rol_usuario=rol_usuario,
        modulo=modulo,
        accion=accion,
        descripcion=descripcion,
        detalle=detalle,
        ip=ip,
    )
    db.add(evento)
    db.commit()


def buscar_eventos(
    db: Session,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    usuario_nombre: Optional[str] = None,
    rol_usuario: Optional[str] = None,
    modulo: Optional[str] = None,
    accion: Optional[str] = None,
) -> List[Auditoria]:
    """
    Busca eventos en la tabla de auditoría con filtros opcionales.
    """
    q = db.query(Auditoria)

    if fecha_desde:
        q = q.filter(Auditoria.fecha_hora >= fecha_desde)
    if fecha_hasta:
        q = q.filter(Auditoria.fecha_hora <= fecha_hasta)
    if usuario_nombre:
        q = q.filter(Auditoria.usuario_nombre.ilike(f"%{usuario_nombre}%"))
    if rol_usuario:
        q = q.filter(Auditoria.rol_usuario == rol_usuario)
    if modulo:
        q = q.filter(Auditoria.modulo == modulo)
    if accion:
        q = q.filter(Auditoria.accion == accion)

    return q.order_by(Auditoria.fecha_hora.desc()).all()
