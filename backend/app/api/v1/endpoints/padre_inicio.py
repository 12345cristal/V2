from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from api.deps import get_current_active_padre
from services.padre_inicio_service import obtener_dashboard_padre
from schemas.padre_inicio import DashboardPadreOut

router = APIRouter(
    prefix="/padre/inicio",
    tags=["Padre - Inicio"]
)


@router.get("/{nino_id}", response_model=DashboardPadreOut)
def inicio_padre(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_padre)
):
    dashboard = obtener_dashboard_padre(db, nino_id)

    if not dashboard:
        raise HTTPException(status_code=404, detail="Niño no encontrado")

    return dashboard
