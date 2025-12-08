"""
IA Service - Integración con Google Gemini para análisis y recomendaciones
"""

from typing import Optional, Dict, Any
import json
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai no está instalado. Funcionalidad de IA deshabilitada.")

from app.core.config import settings
from app.models.decision_log import DecisionLog


class IAService:
    """
    Servicio para integración con Google Gemini AI
    """
    
    def __init__(self):
        """Inicializar servicio de IA"""
        self.gemini_available = GEMINI_AVAILABLE
        self.model = None
        
        if GEMINI_AVAILABLE and settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                print(f"Warning: No se pudo configurar Gemini: {e}")
                self.gemini_available = False
    
    def _verificar_disponibilidad(self):
        """Verificar que el servicio de IA esté disponible"""
        if not self.gemini_available or not self.model:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio de IA no disponible. Verifica GEMINI_API_KEY en .env",
            )
    
    def generar_resumen_progreso_nino(
        self,
        nino_id: int,
        nino_data: Dict[str, Any],
        sesiones_data: list,
        db: Session = None,
        usuario_id: int = None,
    ) -> Dict[str, Any]:
        """
        Generar resumen de progreso del niño usando IA
        
        Args:
            nino_id: ID del niño
            nino_data: Datos del niño (diagnóstico, info emocional, etc.)
            sesiones_data: Lista de sesiones recientes
            db: Session de base de datos (opcional)
            usuario_id: ID del usuario que solicita (opcional)
        
        Returns:
            Dict con resumen generado por IA
        """
        self._verificar_disponibilidad()
        
        try:
            # Construir prompt
            prompt = self._construir_prompt_resumen(nino_data, sesiones_data)
            
            # Llamar a Gemini
            response = self.model.generate_content(prompt)
            resumen = response.text
            
            resultado = {
                "nino_id": nino_id,
                "resumen": resumen,
                "fecha_generacion": datetime.now().isoformat(),
                "n_sesiones_analizadas": len(sesiones_data),
            }
            
            # Log a base de datos
            if db and usuario_id:
                self._log_decision(
                    db=db,
                    usuario_id=usuario_id,
                    tipo="GEMINI_RESUMEN_PROGRESO",
                    contexto=f"Resumen de progreso del niño {nino_id}",
                    entrada={"nino_id": nino_id, "n_sesiones": len(sesiones_data)},
                    salida=resultado,
                )
            
            return resultado
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generando resumen con IA: {str(e)}",
            )
    
    def sugerir_actividades_recursos(
        self,
        nino_id: int,
        perfil_nino: Dict[str, Any],
        recursos_disponibles: list,
        db: Session = None,
        usuario_id: int = None,
    ) -> Dict[str, Any]:
        """
        Sugerir actividades y recursos personalizados para el niño
        
        Args:
            nino_id: ID del niño
            perfil_nino: Perfil completo del niño
            recursos_disponibles: Lista de recursos disponibles
            db: Session de base de datos (opcional)
            usuario_id: ID del usuario que solicita (opcional)
        
        Returns:
            Dict con sugerencias generadas por IA
        """
        self._verificar_disponibilidad()
        
        try:
            # Construir prompt
            prompt = self._construir_prompt_sugerencias(perfil_nino, recursos_disponibles)
            
            # Llamar a Gemini
            response = self.model.generate_content(prompt)
            sugerencias = response.text
            
            resultado = {
                "nino_id": nino_id,
                "sugerencias": sugerencias,
                "fecha_generacion": datetime.now().isoformat(),
                "n_recursos_evaluados": len(recursos_disponibles),
            }
            
            # Log a base de datos
            if db and usuario_id:
                self._log_decision(
                    db=db,
                    usuario_id=usuario_id,
                    tipo="GEMINI_SUGERENCIAS_RECURSOS",
                    contexto=f"Sugerencias de recursos para niño {nino_id}",
                    entrada={"nino_id": nino_id, "n_recursos": len(recursos_disponibles)},
                    salida=resultado,
                )
            
            return resultado
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generando sugerencias con IA: {str(e)}",
            )
    
    def analizar_dashboard(
        self,
        metricas: Dict[str, Any],
        db: Session = None,
        usuario_id: int = None,
    ) -> Dict[str, Any]:
        """
        Analizar métricas del dashboard y generar insights
        
        Args:
            metricas: Métricas del centro (niños, sesiones, terapeutas, etc.)
            db: Session de base de datos (opcional)
            usuario_id: ID del usuario que solicita (opcional)
        
        Returns:
            Dict con análisis e insights generados por IA
        """
        self._verificar_disponibilidad()
        
        try:
            # Construir prompt
            prompt = self._construir_prompt_dashboard(metricas)
            
            # Llamar a Gemini
            response = self.model.generate_content(prompt)
            analisis = response.text
            
            resultado = {
                "analisis": analisis,
                "fecha_generacion": datetime.now().isoformat(),
                "metricas_analizadas": list(metricas.keys()),
            }
            
            # Log a base de datos
            if db and usuario_id:
                self._log_decision(
                    db=db,
                    usuario_id=usuario_id,
                    tipo="GEMINI_DASHBOARD_INSIGHTS",
                    contexto="Análisis de dashboard del centro",
                    entrada={"metricas": metricas},
                    salida=resultado,
                )
            
            return resultado
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generando análisis con IA: {str(e)}",
            )
    
    def _construir_prompt_resumen(
        self,
        nino_data: Dict[str, Any],
        sesiones_data: list,
    ) -> str:
        """Construir prompt para resumen de progreso"""
        prompt = f"""
Eres un especialista en terapias para niños con Trastorno del Espectro Autista (TEA).

**Información del Niño:**
- Nombre: {nino_data.get('nombres', 'N/A')}
- Diagnóstico: {nino_data.get('diagnostico_principal', 'N/A')}
- Edad: {nino_data.get('edad', 'N/A')} años
- Intereses: {nino_data.get('intereses', 'N/A')}
- Conductas desafiantes: {nino_data.get('conductas_desafiantes', 'N/A')}

**Sesiones Recientes ({len(sesiones_data)}):**
"""
        
        for i, sesion in enumerate(sesiones_data[:10], 1):  # Limitar a 10 sesiones
            prompt += f"\n{i}. {sesion.get('fecha', 'N/A')} - {sesion.get('terapia', 'N/A')}"
            prompt += f"\n   Progreso: {sesion.get('progreso', 'N/A')}"
            prompt += f"\n   Observaciones: {sesion.get('observaciones', 'N/A')}"
        
        prompt += """

**Tarea:**
Genera un resumen conciso y profesional del progreso del niño, incluyendo:
1. Análisis de la evolución general
2. Áreas de fortaleza identificadas
3. Áreas que requieren mayor atención
4. Recomendaciones específicas para las próximas sesiones

Usa un lenguaje claro, profesional y empático. Máximo 500 palabras.
"""
        return prompt
    
    def _construir_prompt_sugerencias(
        self,
        perfil_nino: Dict[str, Any],
        recursos_disponibles: list,
    ) -> str:
        """Construir prompt para sugerencias de recursos"""
        prompt = f"""
Eres un especialista en terapias para niños con TEA. 

**Perfil del Niño:**
- Diagnóstico: {perfil_nino.get('diagnostico', 'N/A')}
- Edad: {perfil_nino.get('edad', 'N/A')} años
- Nivel: {perfil_nino.get('nivel', 'N/A')}
- Intereses: {perfil_nino.get('intereses', 'N/A')}
- Objetivos actuales: {perfil_nino.get('objetivos', 'N/A')}

**Recursos Disponibles ({len(recursos_disponibles)}):**
"""
        
        for i, recurso in enumerate(recursos_disponibles[:20], 1):  # Limitar a 20
            prompt += f"\n{i}. {recurso.get('titulo', 'N/A')} ({recurso.get('tipo', 'N/A')})"
            prompt += f"\n   Categoría: {recurso.get('categoria', 'N/A')}"
            prompt += f"\n   Nivel: {recurso.get('nivel', 'N/A')}"
        
        prompt += """

**Tarea:**
Recomienda los 5 recursos más adecuados para este niño, explicando:
1. Por qué cada recurso es apropiado para su perfil
2. Cómo puede ayudar a alcanzar sus objetivos
3. Sugerencias de cómo utilizarlo efectivamente

Sé específico y práctico. Máximo 400 palabras.
"""
        return prompt
    
    def _construir_prompt_dashboard(self, metricas: Dict[str, Any]) -> str:
        """Construir prompt para análisis de dashboard"""
        prompt = f"""
Eres un consultor especializado en gestión de centros de terapias para TEA.

**Métricas del Centro:**
- Total de niños: {metricas.get('total_ninos', 'N/A')}
- Sesiones este mes: {metricas.get('sesiones_mes', 'N/A')}
- Tasa de asistencia: {metricas.get('tasa_asistencia', 'N/A')}%
- Terapeutas activos: {metricas.get('terapeutas_activos', 'N/A')}
- Carga promedio por terapeuta: {metricas.get('carga_promedio', 'N/A')} niños
- Terapias más frecuentes: {metricas.get('terapias_frecuentes', 'N/A')}

**Tarea:**
Genera un análisis ejecutivo del centro, incluyendo:
1. Estado general del centro
2. Fortalezas identificadas
3. Áreas de oportunidad o preocupación
4. Recomendaciones estratégicas accionables

Usa un lenguaje profesional y orientado a la toma de decisiones. Máximo 400 palabras.
"""
        return prompt
    
    def _log_decision(
        self,
        db: Session,
        usuario_id: int,
        tipo: str,
        contexto: str,
        entrada: Dict,
        salida: Dict,
    ) -> None:
        """Guardar log de decisión de IA en base de datos"""
        try:
            log = DecisionLog(
                usuario_id=usuario_id,
                tipo=tipo,
                contexto=contexto,
                entrada_json=json.dumps(entrada, ensure_ascii=False),
                salida_json=json.dumps(salida, ensure_ascii=False),
            )
            
            db.add(log)
            db.commit()
        except Exception as e:
            print(f"Warning: No se pudo guardar log de IA: {e}")


# Instancia global del servicio
ia_service = IAService()
