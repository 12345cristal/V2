from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.notificaciones_service import NotificacionesService
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/notificaciones")


@router.get("/{usuario_id}")
def get_notificaciones(usuario_id: int, db: Session = Depends(get_db),
                       current=Depends(get_current_active_user)):
    # puedes forzar que usuario_id == current.id o que sea admin
    return NotificacionesService.obtener(usuario_id, db)
