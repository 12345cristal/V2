# backend/app/api/v1/endpoints/topsis_terapeutas.py
"""
Endpoint para evaluación TOPSIS de terapeutas
Implementa buenas prácticas REST y manejo robusto de errores
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.schemas.topsis_terapeutas import (
    TopsisEvaluacionRequest,
    TopsisResultado
)
from app.services.topsis_terapeutas_service import TopsisEvaluacionService


router = APIRouter(tags=["TOPSIS - Terapeutas"])


@router.post(
    "/terapeutas",
    response_model=TopsisResultado,
    status_code=status.HTTP_200_OK,
    summary="Evaluar terapeutas con TOPSIS",
    description="""
    Evalúa y rankea terapeutas usando el método TOPSIS (Technique for Order 
    Preference by Similarity to Ideal Solution).
    
    **Criterios evaluados:**
    - Carga laboral (citas activas)
    - Sesiones completadas (experiencia)
    - Rating profesional (promedio de valoraciones)
    - Especialidad (coincidencia con terapia solicitada)
    
    **Pesos:**
    Los pesos deben sumar 1.0 (±0.01 tolerancia).
    Por defecto: carga=0.30, sesiones=0.25, rating=0.30, especialidad=0.15
    
    **Acceso:**
    Solo usuarios con rol COORDINADOR
    """,
    responses={
        200: {
            "description": "Evaluación completada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "total_evaluados": 5,
                        "terapia_solicitada": "Terapia Conductual ABA",
                        "pesos_aplicados": {
                            "carga_laboral": 0.30,
                            "sesiones_completadas": 0.25,
                            "rating": 0.30,
                            "especialidad": 0.15
                        },
                        "ranking": [
                            {
                                "terapeuta_id": 3,
                                "nombre": "Ana Pérez García",
                                "especialidad_principal": "Lenguaje y Comunicación",
                                "score": 0.812,
                                "ranking": 1,
                                "metricas": {
                                    "carga_laboral": 8,
                                    "sesiones_completadas": 45,
                                    "rating": 4.5,
                                    "especialidad_match": True
                                }
                            }
                        ]
                    }
                }
            }
        },
        400: {"description": "Pesos inválidos o suma no es 1.0"},
        401: {"description": "No autenticado"},
        403: {"description": "Sin permisos (requiere rol COORDINADOR)"},
        500: {"description": "Error interno del servidor"}
    }
)
def evaluar_terapeutas_topsis(
    request: TopsisEvaluacionRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> TopsisResultado:
    """
    Evalúa terapeutas usando TOPSIS con datos reales de la base de datos
    """
    try:
        # Debug: imprimir request recibido
        print(f"🔍 DEBUG - Request recibido: {request}")
        print(f"🔍 DEBUG - Pesos: {request.pesos}")
        print(f"🔍 DEBUG - Tipo de pesos: {type(request.pesos)}")
        
        # Inicializar servicio con db session
        service = TopsisEvaluacionService(db)
        
        # Ejecutar evaluación
        resultado = service.evaluar_terapeutas(request)
        
        return resultado
        
    except ValueError as e:
        # Errores de validación (ej: suma de pesos)
        error_msg = str(e)
        print(f"❌ ERROR de validación: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    except Exception as e:
        # Error inesperado - incluir traceback para debugging
        import traceback
        error_detail = f"Error al evaluar terapeutas: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ ERROR TOPSIS: {error_detail}")  # Log en consola
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al evaluar terapeutas: {str(e)}"
        )


@router.get(
    "/terapeutas/pesos-default",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Obtener pesos por defecto",
    description="Retorna los pesos por defecto recomendados para TOPSIS (endpoint público)"
)
def obtener_pesos_default() -> dict:
    """Retorna configuración de pesos por defecto"""
    return {
        "carga_laboral": 0.30,
        "sesiones_completadas": 0.25,
        "rating": 0.30,
        "especialidad": 0.15,
        "descripcion": {
            "carga_laboral": "Número de citas activas (menor = mejor disponibilidad)",
            "sesiones_completadas": "Total de sesiones impartidas (mayor = más experiencia)",
            "rating": "Promedio de valoraciones (mayor = mejor calidad)",
            "especialidad": "Coincidencia con terapia solicitada (1 = domina, 0 = no)"
        }
    }
