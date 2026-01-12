# app/api/v1/endpoints/padre/recursos.py
"""
Router para Recursos Recomendados desde el módulo Padre
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db_session, require_padre
from app.models.usuario import Usuario
from app.models.tutor import Tutor
from app.models.nino import Nino
from app.schemas.padre import Recurso, RecursosListResponse
from app.schemas.enums import TipoRecurso


router = APIRouter()


def verificar_acceso_hijo(hijo_id: int, current_user: Usuario, db: Session) -> Nino:
    """Helper para verificar que el padre tenga acceso al hijo"""
    hijo = db.query(Nino).filter(Nino.id == hijo_id).first()
    if not hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    
    if current_user.rol_id == 4:
        tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
        if not tutor or hijo.tutor_id != tutor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para acceder a esta información"
            )
    
    return hijo


@router.get("/recursos/{hijo_id}", response_model=List[Recurso])
async def listar_recursos(
    hijo_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Lista recursos recomendados para el hijo
    """
    hijo = verificar_acceso_hijo(hijo_id, current_user, db)
    
    # TODO: Implementar modelo y lógica real
    return []


@router.get("/recursos/filtrar", response_model=List[Recurso])
async def filtrar_recursos(
    tipo: Optional[TipoRecurso] = Query(None),
    terapeuta_id: Optional[int] = Query(None),
    objetivo: Optional[str] = Query(None),
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Filtra recursos por tipo, terapeuta u objetivo
    """
    # TODO: Implementar lógica de filtrado
    return []


@router.put("/recursos/{recurso_id}/visto")
async def marcar_recurso_visto(
    recurso_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Marca recurso como visto
    """
    # TODO: Implementar lógica real
    return {"message": "Recurso marcado como visto"}
