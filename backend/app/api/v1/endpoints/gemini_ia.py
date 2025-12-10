# app/api/v1/endpoints/gemini_ia.py
"""
Endpoints para funcionalidades de IA con Gemini
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.usuario import Usuario
from app.models.nino import Nino
from app.services.gemini_service import gemini_service


router = APIRouter()


# ==================== SCHEMAS ====================

class ChatbotRequest(BaseModel):
    """Request para chatbot"""
    mensaje: str = Field(..., description="Pregunta o consulta del usuario")
    nino_id: Optional[int] = Field(None, description="ID del niño para contextualizar")
    incluir_contexto: bool = Field(True, description="Incluir contexto del niño en la consulta")


class ChatbotResponse(BaseModel):
    """Response del chatbot"""
    respuesta: str
    contexto_usado: bool = False
    configurado: bool = True


class ActividadesPersonalizadasRequest(BaseModel):
    """Request para generar actividades"""
    nino_id: int = Field(..., description="ID del niño")
    cantidad: int = Field(5, ge=1, le=10, description="Número de actividades a generar")
    objetivos_especificos: Optional[str] = Field(None, description="Objetivos específicos adicionales")


class ActividadGenerada(BaseModel):
    """Actividad generada por IA"""
    nombre: str
    descripcion: str
    objetivo: str
    duracion_minutos: int
    materiales: List[str]
    nivel_dificultad: str
    area_desarrollo: str


class PlanTerapeuticoRequest(BaseModel):
    """Request para generar plan terapéutico"""
    nino_id: int
    evaluacion_inicial: str = Field(..., description="Evaluación inicial del niño")
    objetivos_padres: Optional[str] = Field(None, description="Objetivos que expresan los padres")


class PlanTerapeuticoResponse(BaseModel):
    """Plan terapéutico generado"""
    objetivos_generales: List[str]
    areas_enfoque: List[str]
    frecuencia_sesiones: str
    terapias_recomendadas: List[Dict[str, str]]
    indicadores_progreso: List[str]
    recomendaciones_padres: List[str]


class AnalisisProgresoRequest(BaseModel):
    """Request para análisis de progreso"""
    nino_id: int
    evaluaciones: List[Dict[str, Any]] = Field(..., description="Lista de evaluaciones realizadas")
    periodo: str = Field("últimos 3 meses", description="Periodo a analizar")


# ==================== ENDPOINTS ====================

@router.post("/chatbot", response_model=ChatbotResponse)
def chatbot_consulta(
    request: ChatbotRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Chatbot de IA para consultas sobre autismo y terapias
    
    Ejemplos de preguntas:
    - "¿Cómo puedo mejorar la comunicación con mi hijo?"
    - "¿Qué actividades son buenas para un niño de 5 años con TEA?"
    - "¿Cómo manejar rabietas en niños con autismo?"
    """
    contexto = None
    contexto_usado = False
    
    # Si se proporciona nino_id y se solicita contexto
    if request.nino_id and request.incluir_contexto:
        nino = db.query(Nino).filter(Nino.id == request.nino_id).first()
        if nino:
            contexto = {
                "nombre": f"{nino.nombre} {nino.apellido_paterno}",
                "edad": nino.edad if hasattr(nino, 'edad') else "No especificada",
                "diagnostico": nino.diagnostico.diagnostico_principal if nino.diagnostico else "No especificado",
                "nivel_autismo": nino.diagnostico.nivel_autismo if nino.diagnostico else "No especificado"
            }
            contexto_usado = True
    
    respuesta = gemini_service.chatbot_consulta(request.mensaje, contexto)
    
    return ChatbotResponse(
        respuesta=respuesta,
        contexto_usado=contexto_usado,
        configurado=gemini_service.configured
    )


@router.post("/actividades-personalizadas", response_model=List[ActividadGenerada])
def generar_actividades_personalizadas(
    request: ActividadesPersonalizadasRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Genera actividades terapéuticas personalizadas usando IA
    
    La IA toma en cuenta:
    - Edad del niño
    - Diagnóstico y nivel de autismo
    - Intereses específicos
    - Objetivos terapéuticos
    """
    # Obtener información del niño
    nino = db.query(Nino).filter(Nino.id == request.nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    # Preparar datos
    nombre = f"{nino.nombre} {nino.apellido_paterno}"
    edad = nino.edad if hasattr(nino, 'edad') else 5
    diagnostico = nino.diagnostico.diagnostico_principal if nino.diagnostico else "TEA"
    nivel = nino.diagnostico.nivel_autismo if nino.diagnostico else "Moderado"
    
    # Obtener intereses si existen
    intereses = None
    if nino.info_emocional and nino.info_emocional.intereses_principales:
        intereses = nino.info_emocional.intereses_principales
    
    # Generar actividades
    actividades = gemini_service.generar_actividades_personalizadas(
        nombre_nino=nombre,
        edad=edad,
        diagnostico=diagnostico,
        nivel_autismo=nivel,
        intereses=intereses,
        objetivos=request.objetivos_especificos,
        cantidad=request.cantidad
    )
    
    return [ActividadGenerada(**act) for act in actividades]


@router.post("/plan-terapeutico", response_model=PlanTerapeuticoResponse)
def generar_plan_terapeutico(
    request: PlanTerapeuticoRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Genera un plan terapéutico completo de 3 meses usando IA
    
    El plan incluye:
    - Objetivos SMART
    - Áreas de enfoque prioritarias
    - Frecuencia de sesiones recomendada
    - Terapias específicas con justificación
    - Indicadores de progreso medibles
    - Recomendaciones para padres
    """
    # Obtener información del niño
    nino = db.query(Nino).filter(Nino.id == request.nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    nombre = f"{nino.nombre} {nino.apellido_paterno}"
    edad = nino.edad if hasattr(nino, 'edad') else 5
    diagnostico = nino.diagnostico.diagnostico_principal if nino.diagnostico else "TEA"
    
    # Generar plan
    plan = gemini_service.generar_plan_terapeutico(
        nombre_nino=nombre,
        edad=edad,
        diagnostico=diagnostico,
        evaluacion_inicial=request.evaluacion_inicial,
        objetivos_padres=request.objetivos_padres
    )
    
    return PlanTerapeuticoResponse(**plan)


@router.post("/analizar-progreso")
def analizar_progreso(
    request: AnalisisProgresoRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Analiza el progreso del niño basado en evaluaciones
    
    Proporciona:
    - Resumen del progreso
    - Áreas de mejora destacadas
    - Áreas que necesitan más trabajo
    - Tendencias observadas
    - Recomendaciones de ajuste al plan
    - Próximos objetivos sugeridos
    - Calificación numérica del progreso
    """
    # Obtener información del niño
    nino = db.query(Nino).filter(Nino.id == request.nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    nombre = f"{nino.nombre} {nino.apellido_paterno}"
    
    # Analizar progreso
    analisis = gemini_service.analizar_progreso(
        nombre_nino=nombre,
        evaluaciones=request.evaluaciones,
        periodo=request.periodo
    )
    
    return analisis


@router.get("/estado")
def estado_gemini(current_user: Usuario = Depends(get_current_user)):
    """
    Verifica el estado de configuración de Gemini AI
    """
    return {
        "configurado": gemini_service.configured,
        "mensaje": "Gemini AI está configurado y funcionando" if gemini_service.configured else "Gemini API KEY no configurada. Funcionalidad limitada.",
        "funcionalidades_disponibles": {
            "chatbot": gemini_service.configured,
            "actividades_personalizadas": gemini_service.configured,
            "plan_terapeutico": gemini_service.configured,
            "analisis_progreso": gemini_service.configured,
            "recomendaciones": True,  # Siempre disponible con fallback
            "embeddings": gemini_service.configured
        }
    }


@router.post("/configurar-api-key")
def configurar_api_key(
    api_key: str = Body(..., embed=True),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Configura la API KEY de Gemini (solo admin)
    
    NOTA: Solo admin puede configurar esto
    """
    if current_user.rol.nombre not in ["admin", "administrador"]:
        raise HTTPException(status_code=403, detail="Solo administradores pueden configurar API keys")
    
    import os
    os.environ["GEMINI_API_KEY"] = api_key
    
    # Reinicializar servicio
    global gemini_service
    from app.services.gemini_service import GeminiService
    gemini_service = GeminiService()
    
    return {
        "success": True,
        "mensaje": "API KEY configurada correctamente" if gemini_service.configured else "Error configurando API KEY",
        "configurado": gemini_service.configured
    }
