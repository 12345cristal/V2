from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_permissions
from app.schemas.coordinador import TerapeutaCargaDetalle
from app.services.coordinador_personal_service import get_detalle_terapeuta

router = APIRouter(
    prefix="/coordinador",
    tags=["coordinador-personal"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("/personal/{id_personal}/detalle-carga", response_model=TerapeutaCargaDetalle)
def detalle_carga_terapeuta(
    id_personal: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["PERSONAL_VER"])),
):
    return get_detalle_terapeuta(db, id_personal=id_personal)
