from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_permissions
from app.models.auditoria import Auditoria
from app.services.auditoria_service import buscar

router = APIRouter(
    prefix="/auditoria",
    tags=["auditoria"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("", response_model=List[dict])
def get_auditoria(
    fecha_desde: Optional[str] = Query(None),
    fecha_hasta: Optional[str] = Query(None),
    usuario: Optional[str] = Query(None),
    modulo: Optional[str] = Query(None),
    accion: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["AUDITORIA_VER"])),
):
    registros = buscar(db, fecha_desde, fecha_hasta, usuario, modulo, accion)
    return [
        {
            "id": r.id,
            "fecha": r.fecha.isoformat(),
            "usuario": r.usuario,
            "rol": r.rol,
            "modulo": r.modulo,
            "accion": r.accion,
            "descripcion": r.descripcion,
            "ip": r.ip,
        }
        for r in registros
    ]
