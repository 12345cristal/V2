from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.core.deps import get_current_active_user
from app.services.ia_service import IAService
from app.models.ninos import Nino

router = APIRouter(prefix="/ia")


class AnalisisNinoDto(BaseModel):
    nino_id: int
    texto_extra: str | None = None


@router.post("/analisis-nino")
def analisis_completo_nino(dto: AnalisisNinoDto,
                           db: Session = Depends(get_db),
                           current=Depends(get_current_active_user)):
    nino = db.query(Nino).filter(Nino.id == dto.nino_id).first()
    if not nino:
        raise HTTPException(404, "Niño no encontrado")
    return IAService.analisis_completo_nino(nino, dto.texto_extra, db, current.id)
