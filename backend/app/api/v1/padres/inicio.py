from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from app.db.session import get_db
from app.api.deps import get_current_padre
from app.schemas.padres_inicio import InicioPadreResponse
from app.services.padres_inicio_service import obtener_inicio_padre

router = APIRouter(
    prefix="/padres",
    tags=["Padres - Inicio"]
)

@router.get("/inicio", response_model=InicioPadreResponse)
def inicio_padre(
    hijo_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_padre),
):
    return obtener_inicio_padre(db, current_user.id, hijo_id)
