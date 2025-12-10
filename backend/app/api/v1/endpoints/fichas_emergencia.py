# app/api/v1/endpoints/fichas_emergencia.py
"""
Endpoints para gestión de Fichas de Emergencia
Accesible para: Administración, Coordinación y Terapeutas
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.services.ficha_emergencia_service import FichaEmergenciaService
from app.schemas.ficha_emergencia import (
    FichaEmergenciaCreate,
    FichaEmergenciaUpdate,
    FichaEmergenciaResponse,
    FichaEmergenciaImprimible
)


router = APIRouter(tags=["Fichas de Emergencia"])


@router.post(
    "/",
    response_model=FichaEmergenciaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear ficha de emergencia",
    description="Crea una nueva ficha de emergencia para un niño"
)
def crear_ficha_emergencia(
    ficha: FichaEmergenciaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> FichaEmergenciaResponse:
    """
    Crea una ficha de emergencia
    Requiere: rol de Administración o Coordinación
    """
    # Verificar permisos
    if current_user.rol not in ["administracion", "coordinacion"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administración y coordinación pueden crear fichas de emergencia"
        )
    
    try:
        service = FichaEmergenciaService(db)
        return service.crear_ficha(ficha, current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creando ficha de emergencia: {str(e)}"
        )


@router.get(
    "/nino/{nino_id}",
    response_model=FichaEmergenciaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener ficha por niño",
    description="Obtiene la ficha de emergencia de un niño específico"
)
def obtener_ficha_por_nino(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> FichaEmergenciaResponse:
    """
    Obtiene ficha de emergencia por ID del niño
    Accesible para: administración, coordinación y terapeutas
    """
    try:
        service = FichaEmergenciaService(db)
        ficha = service.obtener_ficha_por_nino(nino_id)
        
        if not ficha:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe ficha de emergencia para el niño {nino_id}"
            )
        
        return ficha
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo ficha: {str(e)}"
        )


@router.get(
    "/{ficha_id}",
    response_model=FichaEmergenciaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener ficha por ID",
    description="Obtiene una ficha de emergencia por su ID"
)
def obtener_ficha(
    ficha_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> FichaEmergenciaResponse:
    """Obtiene una ficha de emergencia por ID"""
    try:
        service = FichaEmergenciaService(db)
        ficha = service.obtener_ficha_por_id(ficha_id)
        
        if not ficha:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ficha {ficha_id} no encontrada"
            )
        
        return ficha
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo ficha: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[FichaEmergenciaResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todas las fichas",
    description="Lista todas las fichas de emergencia activas"
)
def listar_fichas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> List[FichaEmergenciaResponse]:
    """
    Lista todas las fichas de emergencia activas
    Accesible para todos los roles autenticados
    """
    try:
        service = FichaEmergenciaService(db)
        fichas = service.listar_fichas_activas()
        return fichas
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listando fichas: {str(e)}"
        )


@router.put(
    "/{ficha_id}",
    response_model=FichaEmergenciaResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar ficha",
    description="Actualiza una ficha de emergencia existente"
)
def actualizar_ficha(
    ficha_id: int,
    datos: FichaEmergenciaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> FichaEmergenciaResponse:
    """
    Actualiza una ficha de emergencia
    Requiere: rol de Administración o Coordinación
    """
    # Verificar permisos
    if current_user.rol not in ["administracion", "coordinacion"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administración y coordinación pueden actualizar fichas"
        )
    
    try:
        service = FichaEmergenciaService(db)
        return service.actualizar_ficha(ficha_id, datos)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error actualizando ficha: {str(e)}"
        )


@router.delete(
    "/{ficha_id}",
    status_code=status.HTTP_200_OK,
    summary="Desactivar ficha",
    description="Desactiva una ficha de emergencia (soft delete)"
)
def desactivar_ficha(
    ficha_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Desactiva una ficha de emergencia
    Requiere: rol de Administración
    """
    # Solo administración puede desactivar
    if current_user.rol != "administracion":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administración puede desactivar fichas"
        )
    
    try:
        service = FichaEmergenciaService(db)
        resultado = service.desactivar_ficha(ficha_id)
        
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ficha {ficha_id} no encontrada"
            )
        
        return {"message": "Ficha desactivada exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error desactivando ficha: {str(e)}"
        )


@router.get(
    "/imprimir/nino/{nino_id}",
    response_model=FichaEmergenciaImprimible,
    status_code=status.HTTP_200_OK,
    summary="Obtener ficha para impresión",
    description="Obtiene formato optimizado de ficha para impresión/visualización"
)
def obtener_ficha_imprimible(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> FichaEmergenciaImprimible:
    """
    Obtiene ficha en formato optimizado para impresión
    Incluye foto del niño y toda la información relevante
    """
    try:
        service = FichaEmergenciaService(db)
        return service.obtener_ficha_imprimible(nino_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo ficha imprimible: {str(e)}"
        )
