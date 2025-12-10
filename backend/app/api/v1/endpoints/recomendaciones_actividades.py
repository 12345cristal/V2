# backend/app/api/v1/endpoints/recomendaciones_actividades.py
"""
Endpoints para el sistema de recomendación de actividades basado en contenido
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.services.recomendacion_actividades_service import RecomendacionActividadesService
from app.schemas.recomendacion_actividades import (
    RecomendacionRequest,
    RecomendacionResponse,
    PerfilNinoResponse,
    ProgresoActividadRequest,
    ProgresoActividadResponse
)


router = APIRouter(tags=["Recomendaciones de Actividades"])


@router.get(
    "/test/nino/{nino_id}",
    status_code=status.HTTP_200_OK,
    summary="Test endpoint - verificar perfiles",
    description="Endpoint de prueba para verificar que los perfiles están creados correctamente"
)
def test_perfil_nino(
    nino_id: int,
    db: Session = Depends(get_db)
):
    """Endpoint de prueba sin autenticación para verificar perfiles"""
    try:
        service = RecomendacionActividadesService(db)
        # Acceder directamente al modelo para ver el embedding
        perfil_db = service.obtener_perfil_nino(nino_id)
        
        if not perfil_db:
            return {"error": "No se encontró perfil para este niño", "nino_id": nino_id}
        
        # Verificar embedding
        import json
        embedding_data = json.loads(perfil_db.embedding) if isinstance(perfil_db.embedding, str) else perfil_db.embedding
        
        return {
            "success": True,
            "nino_id": nino_id,
            "tiene_embedding": embedding_data is not None,
            "embedding_dimensiones": len(embedding_data) if embedding_data else 0,
            "edad": perfil_db.edad,
            "diagnosticos": perfil_db.diagnosticos[:2] if perfil_db.diagnosticos else [],
            "dificultades": perfil_db.dificultades[:2] if perfil_db.dificultades else [],
            "fortalezas": perfil_db.fortalezas[:2] if perfil_db.fortalezas else []
        }
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc(), "nino_id": nino_id}


@router.get(
    "/test/recomendaciones/{nino_id}",
    status_code=status.HTTP_200_OK,
    summary="Test endpoint - generar recomendaciones",
    description="Endpoint de prueba para generar recomendaciones sin autenticación"
)
def test_generar_recomendaciones(
    nino_id: int,
    top_n: int = 5,
    db: Session = Depends(get_db)
):
    """Endpoint de prueba para generar recomendaciones sin autenticación"""
    try:
        service = RecomendacionActividadesService(db)
        resultado = service.generar_recomendaciones(
            nino_id=nino_id,
            top_n=top_n,
            filtrar_por_area=None,
            nivel_dificultad_max=None
        )
        
        # Convertir Pydantic model a dict
        resultado_dict = resultado.model_dump()
        
        return {
            "success": True,
            "nino_id": resultado_dict["nino_id"],
            "nombre_nino": resultado_dict["nombre_nino"],
            "total_recomendaciones": resultado_dict["total_recomendaciones"],
            "actividades": [
                {
                    "ranking": act["ranking"],
                    "actividad_id": act["actividad_id"],
                    "nombre": act["nombre"],
                    "score": round(act["score_similitud"], 3),
                    "areas": act["area_desarrollo"],
                    "dificultad": act["dificultad"],
                    "razon": act["razon_recomendacion"]
                }
                for act in resultado_dict["recomendaciones"]
            ]
        }
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc(), "nino_id": nino_id}


@router.post(
    "/generar",
    response_model=RecomendacionResponse,
    status_code=status.HTTP_200_OK,
    summary="Generar recomendaciones de actividades",
    description="""
    Genera recomendaciones personalizadas de actividades para un niño
    basadas en similitud de contenido entre el perfil del niño y las actividades.
    
    **Flujo:**
    1. Obtiene el perfil vectorizado del niño (embeddings)
    2. Obtiene todas las actividades vectorizadas
    3. Calcula similitud coseno entre perfil niño y cada actividad
    4. Ordena por score de similitud (mayor = más recomendada)
    5. Retorna top N actividades con explicación
    
    **Requiere:** Perfil del niño previamente generado
    """
)
def generar_recomendaciones(
    request: RecomendacionRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> RecomendacionResponse:
    """
    Genera recomendaciones de actividades basadas en contenido
    """
    try:
        service = RecomendacionActividadesService(db)
        
        resultado = service.generar_recomendaciones(
            nino_id=request.nino_id,
            top_n=request.top_n,
            filtrar_por_area=request.filtrar_por_area,
            nivel_dificultad_max=request.nivel_dificultad_max
        )
        
        return resultado
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        import traceback
        print(f"❌ ERROR: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando recomendaciones: {str(e)}"
        )


@router.get(
    "/perfil/{nino_id}",
    response_model=PerfilNinoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener perfil de niño",
    description="Retorna el perfil vectorizado y metadatos de un niño"
)
def obtener_perfil_nino(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> PerfilNinoResponse:
    """
    Obtiene el perfil detallado de un niño
    """
    try:
        service = RecomendacionActividadesService(db)
        perfil = service.obtener_perfil_nino_detalle(nino_id)
        return perfil
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo perfil: {str(e)}"
        )


@router.post(
    "/progreso",
    response_model=ProgresoActividadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar progreso en actividad",
    description="""
    Registra el progreso de un niño en una actividad recomendada.
    Esta información se usa para mejorar futuras recomendaciones.
    """
)
def registrar_progreso(
    request: ProgresoActividadRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> ProgresoActividadResponse:
    """
    Registra el progreso de un niño en una actividad
    """
    try:
        service = RecomendacionActividadesService(db)
        
        progreso = service.registrar_progreso(
            nino_id=request.nino_id,
            actividad_id=request.actividad_id,
            terapeuta_id=request.terapeuta_id,
            calificacion=request.calificacion,
            notas_progreso=request.notas_progreso,
            dificultad_encontrada=request.dificultad_encontrada
        )
        
        return ProgresoActividadResponse(
            id=progreso.id,
            nino_id=progreso.nino_id,
            actividad_id=progreso.actividad_id,
            calificacion=progreso.calificacion,
            fecha_registro=progreso.fecha_registro
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registrando progreso: {str(e)}"
        )


@router.get(
    "/quick/{nino_id}",
    response_model=RecomendacionResponse,
    status_code=status.HTTP_200_OK,
    summary="Recomendaciones rápidas (GET)",
    description="Obtiene las 5 mejores recomendaciones de forma rápida"
)
def obtener_recomendaciones_rapidas(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> RecomendacionResponse:
    """
    Endpoint GET simplificado para obtener recomendaciones rápidas
    """
    try:
        service = RecomendacionActividadesService(db)
        
        resultado = service.generar_recomendaciones(
            nino_id=nino_id,
            top_n=5
        )
        
        return resultado
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando recomendaciones: {str(e)}"
        )


@router.get(
    "/historial/{nino_id}",
    status_code=status.HTTP_200_OK,
    summary="Historial de recomendaciones",
    description="Obtiene el historial completo de recomendaciones generadas para un niño"
)
def obtener_historial_recomendaciones(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene todas las recomendaciones históricas generadas para un niño
    """
    try:
        from app.models.recomendacion import RecomendacionActividad
        from sqlalchemy import desc
        
        historial = db.query(RecomendacionActividad)\
            .filter(RecomendacionActividad.nino_id == nino_id)\
            .order_by(desc(RecomendacionActividad.fecha_generacion))\
            .all()
        
        # Enriquecer con nombres de actividades
        resultado = []
        for rec in historial:
            actividades_enriquecidas = []
            for act in rec.actividades_recomendadas:
                # Buscar el nombre de la actividad
                from app.models.actividad import Actividad
                actividad_db = db.query(Actividad).filter(
                    Actividad.id == act.get('actividad_id')
                ).first()
                
                act_info = {
                    "actividad_id": act.get('actividad_id'),
                    "nombre": actividad_db.nombre if actividad_db else None,
                    "score": act.get('score'),
                    "ranking": act.get('ranking'),
                    "razon": act.get('razon')
                }
                actividades_enriquecidas.append(act_info)
            
            resultado.append({
                "id": rec.id,
                "nino_id": rec.nino_id,
                "actividades_recomendadas": actividades_enriquecidas,
                "metodo": rec.metodo,
                "fecha_generacion": rec.fecha_generacion.isoformat() if rec.fecha_generacion else None,
                "aplicada": rec.aplicada
            })
        
        return resultado
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo historial: {str(e)}"
        )
