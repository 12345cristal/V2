"""
Endpoints para IA - Análisis con Google Gemini
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.db.session import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.usuario import Usuario
from app.services.ia_service import ia_service


router = APIRouter()


# ============= SCHEMAS =============

class ResumenProgresoRequest(BaseModel):
    """Request para generar resumen de progreso"""
    nino_id: int = Field(..., description="ID del niño")


class SugerenciasRequest(BaseModel):
    """Request para generar sugerencias de recursos"""
    nino_id: int = Field(..., description="ID del niño")


class AnalisisDashboardResponse(BaseModel):
    """Response para análisis de dashboard"""
    analisis: str
    fecha_generacion: str
    metricas_analizadas: list


# ============= ENDPOINTS =============

@router.post("/ia/resumen-progreso/{nino_id}")
async def generar_resumen_progreso(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
    _: None = Depends(require_permissions("ia:analizar")),
):
    """
    Generar resumen de progreso del niño usando IA (Google Gemini).
    
    **Permisos requeridos:** `ia:analizar`
    
    Analiza las sesiones recientes del niño y genera:
    - Análisis de evolución general
    - Áreas de fortaleza
    - Áreas que requieren atención
    - Recomendaciones específicas
    
    **TODO:** Implementar consulta de datos del niño y sesiones
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint de resumen de progreso pendiente de implementación completa",
    )


@router.post("/ia/sugerencias-recursos/{nino_id}")
async def sugerir_recursos(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
    _: None = Depends(require_permissions("ia:analizar")),
):
    """
    Sugerir actividades y recursos personalizados usando IA.
    
    **Permisos requeridos:** `ia:analizar`
    
    Recomienda los recursos más adecuados según:
    - Diagnóstico y nivel del niño
    - Intereses personales
    - Objetivos actuales
    - Recursos disponibles en el centro
    
    **TODO:** Implementar consulta de perfil del niño y recursos
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint de sugerencias de recursos pendiente de implementación completa",
    )


@router.get("/ia/analizar-dashboard", response_model=AnalisisDashboardResponse)
async def analizar_dashboard(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
    _: None = Depends(require_permissions("ia:analizar")),
):
    """
    Generar insights del dashboard usando IA.
    
    **Permisos requeridos:** `ia:analizar`
    
    Analiza las métricas del centro y genera:
    - Estado general del centro
    - Fortalezas identificadas
    - Áreas de oportunidad
    - Recomendaciones estratégicas
    
    **TODO:** Implementar consulta de métricas del centro
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint de análisis de dashboard pendiente de implementación completa",
    )


@router.get("/ia/status")
async def verificar_status_ia(
    _: Usuario = Depends(get_current_active_user),
):
    """
    Verificar disponibilidad del servicio de IA.
    
    **No requiere permisos especiales.**
    
    Retorna:
    - disponible: bool - Si el servicio está configurado y funcional
    - mensaje: str - Mensaje descriptivo del estado
    """
    if not ia_service.gemini_available:
        return {
            "disponible": False,
            "mensaje": "Servicio de IA no disponible. Verifica GEMINI_API_KEY en .env",
        }
    
    return {
        "disponible": True,
        "mensaje": "Servicio de IA disponible y funcionando correctamente",
    }
