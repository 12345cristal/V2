from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.schemas.topsis_prioridad import PrioridadRequest, NinoPrioritario
from app.services.topsis_prioridad_service import calcular_prioridad_ninos
from app.services.report_service import generar_pdf_prioridad_ninos


router = APIRouter(
    prefix="/decision-support",
    tags=["Decision Support - Prioridad"]
)


# ============================================================
#     ENDPOINT — PRIORIDAD DE NIÑOS (Topsis)
# ============================================================
@router.post("/ninos/prioridad", response_model=List[NinoPrioritario])
def prioridad_ninos(
    body: PrioridadRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user)
):
    """
    Calcula la prioridad de atención de los niños utilizando TOPSIS.

    Solo ADMIN y COORDINADOR pueden acceder.
    """
    if user.rol_sistema not in ("ADMIN", "COORDINADOR"):
        raise HTTPException(status_code=403, detail="No autorizado")

    pesos = {
        "prioridad": body.peso_prioridad,
        "dias_sin_sesion": body.peso_tiempo_espera,
        "asistencias": body.peso_asistencias,
        "inasistencias": body.peso_inasistencias,
    }

    resultados = calcular_prioridad_ninos(db, pesos, body.max_resultados)

    respuesta: List[NinoPrioritario] = []

    for idx, r in enumerate(resultados, start=1):
        n = r["nino"]

        respuesta.append(NinoPrioritario(
            id_nino=n.id_nino,
            nombre_completo=f"{n.nombres} {n.apellido_paterno}",
            score=round(r["score"], 4),
            rank=idx,
            criterios=r["criterios"],
        ))

    return respuesta


# ============================================================
#     ENDPOINT — REPORTE PDF PRIORIDAD DE NIÑOS
# ============================================================
@router.post("/ninos/prioridad/pdf")
def prioridad_ninos_pdf(
    body: PrioridadRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user)
):
    """
    Genera un PDF con el ranking de prioridad de niños evaluados con TOPSIS.
    """
    if user.rol_sistema not in ("ADMIN", "COORDINADOR"):
        raise HTTPException(status_code=403, detail="No autorizado")

    pesos = {
        "prioridad": body.peso_prioridad,
        "dias_sin_sesion": body.peso_tiempo_espera,
        "asistencias": body.peso_asistencias,
        "inasistencias": body.peso_inasistencias,
    }

    resultados = calcular_prioridad_ninos(db, pesos, body.max_resultados)

    pdf_buffer = generar_pdf_prioridad_ninos(resultados)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="prioridad_ninos.pdf"'
        }
    )
