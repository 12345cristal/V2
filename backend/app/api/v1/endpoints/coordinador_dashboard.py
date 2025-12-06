from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.deps import get_db, get_current_active_user, require_permissions
from app.schemas.dashboard_coordinador import DashboardCoordinador
from app.services.dashboard_coordinador_service import build_dashboard

router = APIRouter(
    prefix="/coordinador",
    tags=["coordinador-dashboard"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("/dashboard", response_model=DashboardCoordinador)
def get_dashboard(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["COORDINADOR_DASHBOARD"])),
):
    return build_dashboard(db, fecha=datetime.utcnow())
