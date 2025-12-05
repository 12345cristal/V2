# app/api/v1/endpoints/ia_terapeuta.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_permissions
from app.schemas.ia import ResumenIAResponse
from app.models.bitacora import Bitacora
from app.services.ia_gemini_service import generar_resumen_sesion

router = APIRouter(
    prefix="/terapeutas",
    tags=["IA - Terapeuta"],
)


@router.post("/sesiones/{id_sesion}/resumen-ia", response_model=ResumenIAResponse)
async def generar_resumen_sesion_ia(
    id_sesion: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _=Depends(require_permissions(["IA_SESIONES_RESUMIR"]))
):
    """
    Genera un resumen IA de la última bitácora escrita para esta sesión.
    """

    bitacora = (
        db.query(Bitacora)
        .filter(Bitacora.id_sesion == id_sesion)
        .order_by(Bitacora.creado_en.desc())
        .first()
    )

    if not bitacora:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró bitácora para esta sesión.",
        )

    # TODO: Validar que el terapeuta actual tenga permiso sobre este niño/sesión.

    resumen_texto = await generar_resumen_sesion(bitacora.texto)

    return ResumenIAResponse(resumen=resumen_texto)
