from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.schemas.topsis import (
    RecomendacionTerapeutaRequest,
    TerapeutaRecomendado,
)
from app.services.recomendacion_terapeutas_service import (
    recomendar_terapeutas_para_terapia,
)

router = APIRouter(
    prefix="/decision-support",
    tags=["Decision Support - TOPSIS"],
)


@router.post(
    "/terapeutas/recomendados",
    response_model=List[TerapeutaRecomendado],
)
def recomendar_terapeutas_topsis(
    body: RecomendacionTerapeutaRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user),
):
    # 🔐 Solo ADMIN / COORDINADOR
    if user.rol_sistema not in ("ADMIN", "COORDINADOR"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para usar este módulo de decisión.",
        )

    pesos = {
        "carga": body.peso_carga,
        "sesiones": body.peso_sesiones,
        "rating": body.peso_rating,
        "afinidad": body.peso_afinidad,
    }

    resultados = recomendar_terapeutas_para_terapia(
        db=db,
        id_terapia=body.id_terapia,
        pesos=pesos,
        max_resultados=body.max_resultados,
    )

    respuesta: List[TerapeutaRecomendado] = []
    for idx, r in enumerate(resultados, start=1):
        p = r["personal"]
        criterios = r["criterios"]
        respuesta.append(
            TerapeutaRecomendado(
                id_personal=p.id_personal,
                nombre_completo=f"{p.nombres} {p.apellido_paterno} {p.apellido_materno or ''}".strip(),
                id_terapia=p.id_terapia_principal or body.id_terapia,
                terapia_nombre=p.terapia_principal.nombre
                if p.terapia_principal
                else "",
                score=round(r["score"], 4),
                rank=idx,
                criterios={
                    "carga": criterios["carga"],
                    "sesiones": criterios["sesiones"],
                    "rating": criterios["rating"],
                    "afinidad": criterios["afinidad"],
                },
            )
        )

    return respuesta
