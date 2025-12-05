# app/api/v1/endpoints/ia_ninos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api.deps import get_db, get_current_active_user
from app.schemas.ia_ninos import NinoIAAnalisisResponse
from app.services.ai.ninos_ai_service import analisis_completo_nino

router = APIRouter(
    prefix="/ia/ninos",
    tags=["IA - Niños"],
)


class AnalisisNinoRequest(BaseModel):
    texto_extra: str | None = None


@router.post("/{nino_id}/analisis-completo", response_model=NinoIAAnalisisResponse)
def analizar_nino_completo(
    nino_id: int,
    body: AnalisisNinoRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    IA combinada (A3) para un niño:
    - Lee datos de la BD (diagnóstico, emocional, escolar, terapias, sesiones)
    - Usa texto_extra opcional del terapeuta
    - Llama a Gemini para análisis, recomendaciones, explicación a padres
    """

    # Solo coordinador (2) y terapeuta (3) pueden usar esto
    if current_user.rol_id not in (2, 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para analizar a este niño con IA."
        )

    try:
        resultado = analisis_completo_nino(
            db=db,
            nino_id=nino_id,
            texto_extra=body.texto_extra,
            usuario_id=current_user.id
        )
        return resultado

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
