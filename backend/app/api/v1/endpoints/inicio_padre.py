from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_active_user
from app.services.inicio_padre_service import InicioPadreService

router = APIRouter(prefix="/padres/inicio")


@router.get("")
def obtener_resumen_inicio(db: Session = Depends(get_db),
                           current=Depends(get_current_active_user)):
    return InicioPadreService.obtener_resumen(current, db)
