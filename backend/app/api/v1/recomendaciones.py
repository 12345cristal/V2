# app/api/v1/recomendaciones.py
"""
Endpoints para sistema de recomendaciones inteligentes
Integra: Similitud de contenido + TOPSIS + Gemini
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db, get_current_user
from app.schemas.recomendacion import (
    RecomendacionActividadesResponse,
    SeleccionTerapeutaResponse,
    RecomendacionCompletaResponse,
    GenerarPerfilRequest,
    RegistrarProgresoRequest,
    SugerenciaClinicaRequest,
    SugerenciaClinicaResponse
)
from app.services.recomendacion_service import get_recomendacion_service
from app.models.personal import Personal

router = APIRouter()


@router.post(
    "/actividades/{nino_id}",
    response_model=RecomendacionActividadesResponse,
    summary="Recomendar actividades para un niño",
    description="""
    Genera recomendaciones de actividades terapéuticas basadas en similitud de contenido.
    
    **Proceso:**
    1. Obtiene/genera el perfil vectorizado del niño usando Gemini
    2. Calcula similitud con todas las actividades disponibles
    3. Retorna las top N actividades más similares
    4. Incluye explicación generada por Gemini
    
    **Uso:** Coordinadores y terapeutas pueden usar esto para planificar sesiones
    """
)
def recomendar_actividades_nino(
    nino_id: int,
    top_n: int = 5,
    incluir_explicacion: bool = True,
    db: Session = Depends(get_db),
    current_user: Personal = Depends(get_current_user)
):
    """
    Recomienda actividades terapéuticas para un niño específico
    """
    try:
        servicio = get_recomendacion_service(db)
        resultado = servicio.recomendar_actividades(
            nino_id=nino_id,
            top_n=top_n,
            incluir_explicacion=incluir_explicacion
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


@router.post(
    "/terapeuta/{nino_id}",
    response_model=SeleccionTerapeutaResponse,
    summary="Seleccionar terapeuta óptimo usando TOPSIS",
    description="""
    Selecciona el mejor terapeuta para un niño usando el método TOPSIS.
    
    **Criterios evaluados:**
    - Experiencia (años de práctica)
    - Disponibilidad de horarios
    - Carga de trabajo actual
    - Evaluación de desempeño
    - Nivel de especialización
    
    **Proceso:**
    1. Recopila datos de todos los terapeutas disponibles
    2. Aplica TOPSIS con pesos configurables
    3. Genera ranking ordenado
    4. Gemini explica por qué es la mejor opción
    
    **Uso:** Coordinadores para asignar terapeutas de forma objetiva
    """
)
def seleccionar_terapeuta_optimo(
    nino_id: int,
    terapia_tipo: str,
    criterios_pesos: Optional[dict] = None,
    db: Session = Depends(get_db),
    current_user: Personal = Depends(get_current_user)
):
    """
    Selecciona el terapeuta óptimo usando TOPSIS
    """
    try:
        servicio = get_recomendacion_service(db)
        resultado = servicio.seleccionar_terapeuta_optimo(
            nino_id=nino_id,
            terapia_tipo=terapia_tipo,
            criterios_pesos=criterios_pesos
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
            detail=f"Error seleccionando terapeuta: {str(e)}"
        )


@router.post(
    "/completa/{nino_id}",
    response_model=RecomendacionCompletaResponse,
    summary="Flujo completo de recomendación",
    description="""
    **FLUJO IDEAL COMPLETO:**
    
    1️⃣ **Recomendación basada en contenido** → Sugiere qué terapias y actividades intensificar
    2️⃣ **TOPSIS** → Elige el mejor terapeuta para esas terapias
    3️⃣ **Gemini** → Genera explicación humana para coordinadores y padres
    
    Este endpoint ejecuta todo el proceso de una vez y retorna:
    - Actividades recomendadas con explicación
    - Terapeuta óptimo seleccionado con ranking
    - Justificación clínica completa
    
    **Uso:** Coordinadores para tomar decisiones integrales sobre el tratamiento
    """
)
def recomendacion_completa(
    nino_id: int,
    terapia_tipo: str,
    db: Session = Depends(get_db),
    current_user: Personal = Depends(get_current_user)
):
    """
    Ejecuta el flujo completo de recomendación
    """
    try:
        servicio = get_recomendacion_service(db)
        resultado = servicio.flujo_completo_recomendacion(
            nino_id=nino_id,
            terapia_tipo=terapia_tipo
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
            detail=f"Error en flujo completo: {str(e)}"
        )


@router.post(
    "/perfil/generar",
    summary="Generar o actualizar perfil vectorizado",
    description="""
    Genera/actualiza el perfil vectorizado de un niño usando Gemini.
    
    El perfil incluye:
    - Embeddings de características clínicas
    - Diagnósticos estructurados
    - Dificultades y fortalezas
    - Notas clínicas vectorizadas
    
    **Uso:** Se ejecuta automáticamente al recomendar, pero puede forzarse manualmente
    """
)
def generar_perfil_vectorizado(
    request: GenerarPerfilRequest,
    db: Session = Depends(get_db),
    current_user: Personal = Depends(get_current_user)
):
    """
    Genera o actualiza el perfil vectorizado de un niño
    """
    try:
        servicio = get_recomendacion_service(db)
        perfil = servicio.crear_perfil_nino(nino_id=request.nino_id)
        
        return {
            "nino_id": perfil.nino_id,
            "edad": perfil.edad,
            "diagnosticos": perfil.diagnosticos,
            "dificultades": perfil.dificultades,
            "fortalezas": perfil.fortalezas,
            "fecha_generacion": perfil.fecha_generacion.isoformat(),
            "fecha_actualizacion": perfil.fecha_actualizacion.isoformat(),
            "embedding_dimension": len(perfil.embedding) if perfil.embedding else 0
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando perfil: {str(e)}"
        )


@router.post(
    "/progreso/registrar",
    summary="Registrar progreso en actividad",
    description="""
    Registra el progreso de un niño en una actividad terapéutica.
    
    Este dato se usa para:
    - Aprendizaje colaborativo (qué actividades funcionan mejor)
    - Análisis de efectividad
    - Ajuste de recomendaciones futuras
    
    **Uso:** Terapeutas registran después de cada sesión
    """
)
def registrar_progreso_actividad(
    request: RegistrarProgresoRequest,
    db: Session = Depends(get_db),
    current_user: Personal = Depends(get_current_user)
):
    """
    Registra progreso de un niño en una actividad
    """
    from app.models.recomendacion import HistorialProgreso
    from datetime import datetime
    
    try:
        # Crear registro de progreso
        progreso = HistorialProgreso(
            nino_id=request.nino_id,
            actividad_id=request.actividad_id,
            terapeuta_id=request.terapeuta_id,
            calificacion=request.calificacion,
            notas_progreso=request.notas_progreso,
            duracion_minutos=request.duracion_minutos,
            fecha_sesion=datetime.utcnow()
        )
        
        # Si hay notas, generar embedding
        if request.notas_progreso:
            from app.services.gemini_service import gemini_service
            embedding = gemini_service.generar_embedding(request.notas_progreso)
            progreso.embedding_notas = embedding
        
        db.add(progreso)
        db.commit()
        db.refresh(progreso)
        
        return {
            "success": True,
            "progreso_id": progreso.id,
            "mensaje": "Progreso registrado exitosamente"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registrando progreso: {str(e)}"
        )


@router.post(
    "/sugerencias/{nino_id}",
    response_model=SugerenciaClinicaResponse,
    summary="Generar sugerencias clínicas con Gemini",
    description="""
    Usa Gemini para generar sugerencias clínicas personalizadas.
    
    Gemini analiza:
    - Perfil completo del niño
    - Actividades actuales
    - Progreso reciente
    - Patrones identificados
    
    Y genera sugerencias específicas y accionables.
    
    **Uso:** Terapeutas y coordinadores para optimizar planes de tratamiento
    """
)
def generar_sugerencias_clinicas(
    nino_id: int,
    request: SugerenciaClinicaRequest,
    db: Session = Depends(get_db),
    current_user: Personal = Depends(get_current_user)
):
    """
    Genera sugerencias clínicas usando Gemini
    """
    from app.models.recomendacion import PerfilNinoVectorizado, HistorialProgreso
    from app.models.actividad import Actividad
    from app.services.gemini_service import gemini_service
    from datetime import datetime, timedelta
    
    try:
        # Obtener perfil del niño
        perfil = db.query(PerfilNinoVectorizado).filter(
            PerfilNinoVectorizado.nino_id == nino_id
        ).first()
        
        if not perfil:
            raise ValueError(f"Perfil del niño {nino_id} no encontrado")
        
        # Obtener actividades recientes
        actividades_actuales = []
        if request.incluir_actividades_actuales:
            fecha_limite = datetime.utcnow() - timedelta(days=30)
            progresos = db.query(HistorialProgreso).filter(
                HistorialProgreso.nino_id == nino_id,
                HistorialProgreso.fecha_sesion >= fecha_limite
            ).all()
            
            actividades_ids = list(set([p.actividad_id for p in progresos]))
            actividades = db.query(Actividad).filter(
                Actividad.id.in_(actividades_ids)
            ).all()
            actividades_actuales = [act.nombre for act in actividades]
        
        # Obtener progreso reciente
        progreso_texto = ""
        if request.incluir_progreso_reciente:
            fecha_limite = datetime.utcnow() - timedelta(days=14)
            progresos_recientes = db.query(HistorialProgreso).filter(
                HistorialProgreso.nino_id == nino_id,
                HistorialProgreso.fecha_sesion >= fecha_limite,
                HistorialProgreso.notas_progreso.isnot(None)
            ).order_by(HistorialProgreso.fecha_sesion.desc()).limit(5).all()
            
            notas = [p.notas_progreso for p in progresos_recientes if p.notas_progreso]
            progreso_texto = " | ".join(notas)
        
        # Generar sugerencias con Gemini
        sugerencias = gemini_service.generar_sugerencias_clinicas(
            perfil_nino=perfil.texto_perfil,
            actividades_actuales=actividades_actuales,
            progreso_reciente=progreso_texto
        )
        
        return {
            "nino_id": nino_id,
            "sugerencias": sugerencias,
            "contexto_usado": {
                "actividades_actuales": actividades_actuales,
                "progreso_incluido": bool(progreso_texto)
            },
            "fecha_generacion": datetime.utcnow().isoformat()
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando sugerencias: {str(e)}"
        )


@router.get(
    "/historial/{nino_id}",
    summary="Obtener historial de recomendaciones",
    description="Retorna el historial de recomendaciones generadas para un niño"
)
def obtener_historial_recomendaciones(
    nino_id: int,
    limite: int = 10,
    db: Session = Depends(get_db),
    current_user: Personal = Depends(get_current_user)
):
    """
    Obtiene el historial de recomendaciones
    """
    from app.models.recomendacion import RecomendacionActividad
    
    recomendaciones = db.query(RecomendacionActividad).filter(
        RecomendacionActividad.nino_id == nino_id
    ).order_by(
        RecomendacionActividad.fecha_generacion.desc()
    ).limit(limite).all()
    
    return {
        "nino_id": nino_id,
        "total": len(recomendaciones),
        "recomendaciones": [
            {
                "id": rec.id,
                "fecha": rec.fecha_generacion.isoformat(),
                "metodo": rec.metodo,
                "num_actividades": len(rec.actividades_recomendadas),
                "aplicada": bool(rec.aplicada)
            }
            for rec in recomendaciones
        ]
    }
