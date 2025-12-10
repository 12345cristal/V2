# app/api/v1/endpoints/recomendacion.py
"""
Endpoints para el módulo de Recomendación Basada en Contenido
Permite al COORDINADOR y TERAPEUTA obtener recomendaciones personalizadas
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.schemas.recomendacion import RecomendacionActividad, RecomendacionTerapia
from app.services import recommend_service


router = APIRouter(tags=["Recomendación"])


# ============================================================
# ENDPOINTS PARA RECOMENDACIONES
# ============================================================

@router.get("/actividades/{nino_id}", response_model=List[RecomendacionActividad])
def get_recomendacion_actividades(
    nino_id: int,
    top_n: int = Query(10, ge=1, le=50, description="Número de recomendaciones a retornar"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene recomendaciones de actividades para un niño específico
    
    Utiliza similitud de contenido entre:
    - Perfil del niño (diagnóstico, preferencias, dificultades)
    - Características de las actividades (tags, área de desarrollo, objetivo)
    
    Accesible para COORDINADOR y TERAPEUTA
    """
    try:
        recomendaciones = recommend_service.recomendar_actividades_para_nino(
            db,
            nino_id,
            top_n
        )
        return recomendaciones
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar recomendaciones: {str(e)}"
        )


@router.get("/terapias/{nino_id}", response_model=List[RecomendacionTerapia])
def get_recomendacion_terapias(
    nino_id: int,
    top_n: int = Query(10, ge=1, le=50, description="Número de recomendaciones a retornar"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene recomendaciones de terapias para un niño específico
    
    Utiliza similitud de contenido entre:
    - Perfil del niño (diagnóstico, preferencias, dificultades)
    - Características de las terapias (tags, categoría, objetivo)
    
    Accesible para COORDINADOR y TERAPEUTA
    """
    try:
        recomendaciones = recommend_service.recomendar_terapias_para_nino(
            db,
            nino_id,
            top_n
        )
        return recomendaciones
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar recomendaciones: {str(e)}"
        )
