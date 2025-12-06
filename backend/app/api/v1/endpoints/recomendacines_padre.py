from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_permissions
from app.schemas.recurso_terapeuta import RecursoTerapeutaRead
from app.services.ia_recomendacion_service import recomendar_recursos_para_nino

router = APIRouter(
    prefix="/padres",
    tags=["padres-recomendaciones"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("/{id_nino}/recomendaciones", response_model=List[RecursoTerapeutaRead])
def recomendaciones_para_nino(
    id_nino: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["PADRE_VER_RECURSOS"])),
):
    recursos = recomendar_recursos_para_nino(db, id_nino=id_nino, top_k=5)
    return recursos
