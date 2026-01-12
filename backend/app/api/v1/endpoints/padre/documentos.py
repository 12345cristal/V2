# app/api/v1/endpoints/padre/documentos.py
"""
Router para gestión de Documentos desde el módulo Padre
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db_session, require_padre
from app.models.usuario import Usuario
from app.models.tutor import Tutor
from app.models.nino import Nino
from app.schemas.padre import Documento, DocumentosListResponse


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


@router.get("/documentos/{hijo_id}", response_model=List[Documento])
async def listar_documentos(
    hijo_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Lista documentos del hijo
    """
    hijo = verificar_acceso_hijo(hijo_id, current_user, db)
    
    # TODO: Implementar modelo y lógica real
    return []


@router.get("/documentos/detalle/{documento_id}")
async def descargar_documento(
    documento_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Descarga o visualiza documento PDF
    """
    # TODO: Implementar lógica real
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Documento no encontrado"
    )


@router.put("/documentos/{documento_id}/leido")
async def marcar_documento_leido(
    documento_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Marca documento como visto
    """
    # TODO: Implementar lógica real
    return {"message": "Documento marcado como leído"}


@router.get("/documentos/{documento_id}/preview")
async def preview_documento(
    documento_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Preview del documento PDF
    """
    # TODO: Implementar lógica real
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad en desarrollo"
    )
