from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_permissions
from app.models.personal import Personal
from app.services.topsis_service import topsis

router = APIRouter(
    prefix="/coordinador/topsis",
    tags=["topsis"],
    dependencies=[Depends(get_current_active_user)],
)


class TerapeutaTopsisItem(BaseModel):
  id_personal: int
  nombre_completo: str
  especialidad: str
  score: float


@router.get("/terapeutas", response_model=List[TerapeutaTopsisItem])
def ranking_terapeutas_para_terapia(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["TERAPIAS_ASIGNAR"])),
):
    # criterio ejemplo:
    # [carga_actual (menos mejor), sesiones_semana (menos mejor), rating (más mejor)]
    terapeutas = (
        db.query(Personal)
        .filter(Personal.estado_laboral == "ACTIVO")
        .all()
    )
    if not terapeutas:
        return []

    matriz = []
    for t in terapeutas:
        carga = t.total_pacientes or 0
        sesiones = t.sesiones_semana or 0
        rating = t.rating or 0
        matriz.append([carga, sesiones, rating])

    pesos = [0.4, 0.3, 0.3]
    criterios_beneficio = [False, False, True]

    scores = topsis(matriz, pesos, criterios_beneficio)

    items = []
    for t, s in zip(terapeutas, scores):
        items.append(
            TerapeutaTopsisItem(
                id_personal=t.id_personal,
                nombre_completo=f"{t.nombres} {t.apellido_paterno} {t.apellido_materno or ''}".strip(),
                especialidad=t.especialidad_principal,
                score=round(s, 4),
            )
        )

    # ordenar de mayor score a menor
    items.sort(key=lambda x: x.score, reverse=True)
    return items
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_permissions
from app.models.personal import Personal
from app.services.topsis_service import topsis

router = APIRouter(
    prefix="/coordinador/topsis",
    tags=["topsis"],
    dependencies=[Depends(get_current_active_user)],
)


class TerapeutaTopsisItem(BaseModel):
  id_personal: int
  nombre_completo: str
  especialidad: str
  score: float


@router.get("/terapeutas", response_model=List[TerapeutaTopsisItem])
def ranking_terapeutas_para_terapia(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["TERAPIAS_ASIGNAR"])),
):
    # criterio ejemplo:
    # [carga_actual (menos mejor), sesiones_semana (menos mejor), rating (más mejor)]
    terapeutas = (
        db.query(Personal)
        .filter(Personal.estado_laboral == "ACTIVO")
        .all()
    )
    if not terapeutas:
        return []

    matriz = []
    for t in terapeutas:
        carga = t.total_pacientes or 0
        sesiones = t.sesiones_semana or 0
        rating = t.rating or 0
        matriz.append([carga, sesiones, rating])

    pesos = [0.4, 0.3, 0.3]
    criterios_beneficio = [False, False, True]

    scores = topsis(matriz, pesos, criterios_beneficio)

    items = []
    for t, s in zip(terapeutas, scores):
        items.append(
            TerapeutaTopsisItem(
                id_personal=t.id_personal,
                nombre_completo=f"{t.nombres} {t.apellido_paterno} {t.apellido_materno or ''}".strip(),
                especialidad=t.especialidad_principal,
                score=round(s, 4),
            )
        )

    # ordenar de mayor score a menor
    items.sort(key=lambda x: x.score, reverse=True)
    return items
