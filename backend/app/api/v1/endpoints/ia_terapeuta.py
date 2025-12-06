# app/api/v1/endpoints/ia_terapeuta.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict

from app.api.deps import get_db, get_current_active_user, require_permissions
from app.models.bitacora import Bitacora
from app.schemas.ia import ResumenIAResponse
from app.services.ia_gemini_service import generar_resumen_sesion

router = APIRouter(
    prefix="/terapeutas",
    tags=["IA - Terapeuta"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("/sesiones/{id_sesion}/resumen-ia", response_model=ResumenIAResponse)
async def resumen_ia_sesion(
    id_sesion: int,
    db: Session = Depends(get_db),
    user: Dict = Depends(get_current_active_user),
    _: Dict = Depends(require_permissions(["IA_SESIONES_RESUMIR"])),
):
    """
    Genera un resumen de IA basado en la bitácora más reciente de la sesión.
    - Solo terapeutas asignados o roles con permisos pueden acceder.
    - Guarda el resumen generado en la base de datos.
    """

    # 1️⃣ Obtener la bitácora más reciente de la sesión
    bitacora: Bitacora = (
        db.query(Bitacora)
        .filter(Bitacora.id_sesion == id_sesion)
        .order_by(Bitacora.creado_en.desc())
        .first()
    )

    if not bitacora or not getattr(bitacora, "texto", None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay texto de sesión disponible para resumir.",
        )

    # 2️⃣ Validar acceso del terapeuta
    if user.get("rol_sistema") == "TERAPEUTA" and bitacora.id_terapeuta != user.get("id_personal"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes acceder a bitácoras de niños que no atiendes."
        )

    # 3️⃣ Generar resumen IA
    resumen_texto: str = await generar_resumen_sesion(bitacora.texto)

    # 4️⃣ Guardar resumen en la bitácora (opcional, recomendado)
    bitacora.resumen_ia = resumen_texto
    db.add(bitacora)
    db.commit()
    db.refresh(bitacora)

    return ResumenIAResponse(resumen=resumen_texto)
