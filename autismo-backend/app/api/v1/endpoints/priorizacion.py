"""
Endpoints para priorización usando TOPSIS
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.db.session import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.usuario import Usuario
from app.services.topsis_service import topsis_service


router = APIRouter()


# ============= SCHEMAS =============

class Criterio(BaseModel):
    """Schema para criterio de TOPSIS"""
    nombre: str = Field(..., description="Nombre del criterio")
    peso: float = Field(..., gt=0, description="Peso del criterio (mayor a 0)")
    tipo: str = Field(..., pattern="^(beneficio|costo)$", description="Tipo: 'beneficio' o 'costo'")


class Alternativa(BaseModel):
    """Schema para alternativa de TOPSIS"""
    id: int = Field(..., description="ID de la alternativa")
    nombre: str = Field(None, description="Nombre descriptivo (opcional)")
    valores: List[float] = Field(..., description="Valores para cada criterio (mismo orden que criterios)")


class TOPSISRequest(BaseModel):
    """Schema para request de TOPSIS"""
    criterios: List[Criterio] = Field(..., min_items=1, description="Lista de criterios")
    alternativas: List[Alternativa] = Field(..., min_items=1, description="Lista de alternativas")
    contexto: str = Field(None, description="Descripción del contexto (opcional)")


class TOPSISResultado(BaseModel):
    """Schema para resultado de TOPSIS"""
    id: int
    nombre: str
    score: float
    ranking: int
    valores: List[float]


class TOPSISResponse(BaseModel):
    """Schema para respuesta de TOPSIS"""
    resultados: List[TOPSISResultado]
    mejor_alternativa: TOPSISResultado
    contexto: str = None


# ============= ENDPOINTS =============

@router.post("/priorizacion/topsis", response_model=TOPSISResponse)
async def ejecutar_topsis(
    request: TOPSISRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
    _: None = Depends(require_permissions("priorizacion:ejecutar")),
):
    """
    Ejecutar algoritmo TOPSIS genérico.
    
    **Permisos requeridos:** `priorizacion:ejecutar`
    
    **TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)**
    
    Algoritmo de toma de decisiones multi-criterio que:
    1. Normaliza los valores de las alternativas
    2. Aplica pesos a los criterios
    3. Calcula soluciones ideales positiva y negativa
    4. Determina qué alternativa está más cerca de la ideal positiva
    
    **Ejemplo de uso:**
    ```json
    {
      "criterios": [
        {"nombre": "Experiencia (años)", "peso": 0.4, "tipo": "beneficio"},
        {"nombre": "Carga actual (niños)", "peso": 0.3, "tipo": "costo"},
        {"nombre": "Especialización", "peso": 0.3, "tipo": "beneficio"}
      ],
      "alternativas": [
        {"id": 1, "nombre": "Terapeuta A", "valores": [5, 8, 7]},
        {"id": 2, "nombre": "Terapeuta B", "valores": [8, 3, 6]},
        {"id": 3, "nombre": "Terapeuta C", "valores": [3, 5, 9]}
      ],
      "contexto": "Selección de terapeuta para niño con TEA severo"
    }
    ```
    
    **Retorna:** Alternativas ordenadas por score (0-1), donde 1 es la mejor opción.
    """
    # Convertir a formato dict para el servicio
    criterios_dict = [c.model_dump() for c in request.criterios]
    alternativas_dict = [a.model_dump() for a in request.alternativas]
    
    # Ejecutar TOPSIS
    resultados = topsis_service.ejecutar_topsis(
        criterios=criterios_dict,
        alternativas=alternativas_dict,
        db=db,
        usuario_id=current_user.id,
        contexto=request.contexto,
    )
    
    return {
        "resultados": resultados,
        "mejor_alternativa": resultados[0] if resultados else None,
        "contexto": request.contexto,
    }


@router.post("/priorizacion/ninos")
async def priorizar_ninos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
    _: None = Depends(require_permissions("priorizacion:ejecutar")),
):
    """
    Priorizar niños para atención usando TOPSIS.
    
    **Permisos requeridos:** `priorizacion:ejecutar`
    
    **Criterios considerados:**
    - Severidad del diagnóstico
    - Tiempo sin terapia
    - Edad del niño
    - Disponibilidad de recursos
    
    **TODO:** Implementar lógica específica para priorización de niños
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint de priorización de niños pendiente de implementación",
    )


@router.post("/priorizacion/terapeutas")
async def priorizar_terapeutas(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
    _: None = Depends(require_permissions("priorizacion:ejecutar")),
):
    """
    Seleccionar mejor terapeuta para un niño usando TOPSIS.
    
    **Permisos requeridos:** `priorizacion:ejecutar`
    
    **Criterios considerados:**
    - Años de experiencia
    - Especialización en el diagnóstico del niño
    - Carga actual de niños
    - Disponibilidad horaria
    - Historial de éxito
    
    **TODO:** Implementar lógica específica para selección de terapeutas
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint de priorización de terapeutas pendiente de implementación",
    )


@router.get("/priorizacion/logs")
async def obtener_logs_priorizacion(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("priorizacion:ver_logs")),
):
    """
    Obtener historial de ejecuciones de TOPSIS.
    
    **Permisos requeridos:** `priorizacion:ver_logs`
    
    **TODO:** Implementar consulta a decision_logs
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint de logs de priorización pendiente de implementación",
    )
