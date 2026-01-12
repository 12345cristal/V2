# app/api/v1/padres/mis_hijos.py
from fastapi import APIRouter, Depends, Path, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_padre
from app.schemas.padres_mis_hijos import MisHijosApiResponse
from app.services.padres_mis_hijos_service import (
    obtener_mis_hijos,
    obtener_hijo_por_id,
    marcar_medicamento_como_visto
)

router = APIRouter(
    prefix="/padres",
    tags=["Padres - Mis Hijos"]
)


@router.get("/mis-hijos", response_model=MisHijosApiResponse)
def get_mis_hijos(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_padre),
):
    """
    Obtiene todos los hijos del padre con su información clínica y administrativa.
    
    Incluye:
    - Foto, nombre, edad calculada
    - Diagnóstico y cuatrimestre
    - Fecha de ingreso
    - Alergias (solo lectura)
    - Medicamentos actuales
    - Estados: visto/no visto
    """
    return obtener_mis_hijos(current_user.id, db)


@router.get("/mis-hijos/{nino_id}", response_model=MisHijosApiResponse)
def get_hijo_detalle(
    nino_id: int = Path(..., description="ID del niño"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_padre),
):
    """
    Obtiene los detalles completos de un hijo específico.
    """
    return obtener_hijo_por_id(current_user.id, nino_id, db)


@router.put("/mis-hijos/{nino_id}/medicamentos/{medicamento_id}/visto")
def marcar_medicamento_visto(
    nino_id: int = Path(..., description="ID del niño"),
    medicamento_id: int = Path(..., description="ID del medicamento"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_padre),
):
    """
    Marca un medicamento como visto (quita la novedad).
    """
    return marcar_medicamento_como_visto(current_user.id, nino_id, medicamento_id, db)
