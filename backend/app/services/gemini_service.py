"""
LEGACY: Mantiene compatibilidad hacia atrás con módulos existentes.
Para nuevo código, usa:
  - gemini_chat_service: chat terapéutico
  - gemini_embedding_service: embeddings y similitud
"""

from __future__ import annotations

from typing import List, Dict, Optional
import google.generativeai as genai

from app.core.config import settings
from app.services.gemini_chat_service import gemini_chat_service


# =====================================================
# COMPATIBILIDAD HACIA ATRÁS
# =====================================================
class GeminiService:
    """
    DEPRECATED: Mantiene compatibilidad con código existente.
    
    Usa en su lugar:
    - gemini_chat_service.chat() → para chatbot
    - gemini_embedding_service.embed() → para embeddings
    """

    def __init__(self):
        self.is_configured = False
        
        if not settings.GEMINI_API_KEY:
            print("⚠ ADVERTENCIA: GEMINI_API_KEY no está configurada")
            return
        
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model_name = settings.GEMINI_MODEL
            self.model = genai.GenerativeModel(self.model_name)
            self.is_configured = True
        except Exception as e:
            print(f"⚠ Error al configurar Gemini: {str(e)}")
    
    # ----- Chatbot (delegado) -----
    def chat(
        self,
        mensaje: str,
        *,
        contexto_nino: Dict = None,
        historial: List[Dict[str, str]] = None,
    ) -> str:
        """
        DEPRECATED: Usa gemini_chat_service.chat() en su lugar.
        
        Mantiene compatibilidad con interface antiguo.
        """
        result = self.chat_service.chat(
            mensaje,
            contexto_nino=contexto_nino,
        )
        return result.get("respuesta", "")

    # ----- Embeddings (delegado) -----
    def generar_embedding(self, texto: str) -> List[float]:
        """
        DEPRECATED: Usa gemini_embedding_service.embed() en su lugar.
        """
        return self.embedding_service.embed(texto)

    def generar_embedding_perfil_nino(
        self, datos_nino: Dict
    ) -> tuple[List[float], str]:
        """
        DEPRECATED: Usa gemini_embedding_service.embed_perfil_nino() en su lugar.
        """
        return self.embedding_service.embed_perfil_nino(datos_nino)

    def generar_embedding_actividad(
        self, datos_actividad: Dict
    ) -> tuple[List[float], str]:
        """
        DEPRECATED: Usa gemini_embedding_service.embed_actividad() en su lugar.
        """
        return self.embedding_service.embed_actividad(datos_actividad)

    def calcular_similitud_coseno(
        self, vector1: List[float], vector2: List[float]
    ) -> float:
        """
        DEPRECATED: Usa gemini_embedding_service.similitud_coseno() en su lugar.
        """
        return self.embedding_service.similitud_coseno(vector1, vector2)

    # ----- Fallbacks clínicos -----
    @staticmethod
    def _fallback_response(mensaje: str) -> str:
        """Respuesta clínica segura."""
        return (
            "Puedo darte orientación general basada en buenas prácticas:\n\n"
            "• Mantén rutinas predecibles y anticipa cambios.\n"
            "• Usa apoyos visuales y lenguaje claro.\n"
            "• Refuerza positivamente conductas adecuadas.\n"
            "• Divide actividades en pasos pequeños.\n"
            "• Ante rabietas: mantén la calma, valida la emoción y ofrece espacio tranquilo.\n\n"
            "Si deseas recomendaciones más específicas, indica edad, nivel de apoyo y objetivo terapéutico."
        )

    # ----- Plantillas por defecto -----
    @staticmethod
    def actividades_por_defecto() -> List[Dict]:
        """Plantilla de actividades si no hay datos."""
        return [
            {
                "nombre": "Juego de imitación",
                "descripcion": "Actividad para desarrollar habilidades sociales mediante imitación de gestos y expresiones faciales.",
                "objetivo": "Mejorar la comunicación no verbal y habilidades de imitación",
                "duracion_minutos": 20,
                "materiales": ["Espejo", "Imágenes de emociones", "Tarjetas visuales"],
                "nivel_dificultad": "Básico",
                "area_desarrollo": "Social",
            },
            {
                "nombre": "Rutina sensorial",
                "descripcion": "Actividades táctiles con diferentes texturas para estimulación sensorial controlada.",
                "objetivo": "Regular procesamiento sensorial y reducir hipersensibilidad",
                "duracion_minutos": 30,
                "materiales": ["Plastilina", "Arena kinética", "Pelotas texturizadas", "Telas suaves"],
                "nivel_dificultad": "Básico",
                "area_desarrollo": "Sensorial",
            },
            {
                "nombre": "Construcción con bloques",
                "descripcion": "Actividad de construcción guiada que promueve la planificación motora y seguimiento de instrucciones.",
                "objetivo": "Desarrollar habilidades motoras finas y planificación secuencial",
                "duracion_minutos": 25,
                "materiales": ["Bloques de construcción", "Imágenes de referencia", "Contenedor organizador"],
                "nivel_dificultad": "Intermedio",
                "area_desarrollo": "Motora",
            },
        ]

    @staticmethod
    def plan_por_defecto() -> Dict:
        """Plantilla de plan terapéutico."""
        return {
            "objetivos_generales": [
                "Mejorar habilidades de comunicación verbal y no verbal",
                "Desarrollar mayor interacción social con pares",
                "Fortalecer capacidades de autorregulación emocional",
            ],
            "areas_enfoque": ["Comunicación", "Social", "Sensorial", "Emocional"],
            "frecuencia_sesiones": "2-3 veces por semana (sesiones de 45-60 minutos)",
            "terapias_recomendadas": [
                {
                    "tipo": "Terapia de Lenguaje",
                    "justificacion": "Mejorar comunicación expresiva y receptiva",
                },
                {
                    "tipo": "Terapia Ocupacional",
                    "justificacion": "Trabajar integración sensorial y habilidades motoras",
                },
                {
                    "tipo": "Terapia Conductual (ABA)",
                    "justificacion": "Desarrollar habilidades sociales y reducir conductas desafiantes",
                },
            ],
            "indicadores_progreso": [
                "Aumento en palabras expresadas por sesión",
                "Mejora en contacto visual sostenido",
                "Reducción de episodios de desregulación",
                "Mayor tiempo de atención en actividades estructuradas",
            ],
            "recomendaciones_padres": [
                "Practicar actividades de comunicación en casa diariamente",
                "Mantener rutinas consistentes y predecibles",
                "Reforzar positivamente logros pequeños",
                "Crear un ambiente sensorial adecuado en el hogar",
            ],
        }

    async def generate_recomendacion(self, nino_data: dict) -> str:
        """Genera una recomendación personalizada para un niño"""
        if not self.is_configured:
            raise ValueError("Servicio Gemini no está configurado")
            
        try:
            prompt = f"""
Basándote en la siguiente información del niño, genera una recomendación educativa personalizada:

Nombre: {nino_data.get('nombre', 'No especificado')}
Edad: {nino_data.get('edad', 'No especificada')}
Grado: {nino_data.get('grado', 'No especificado')}
Áreas de fortaleza: {nino_data.get('fortalezas', 'No especificadas')}
Áreas de mejora: {nino_data.get('areas_mejora', 'No especificadas')}
Intereses: {nino_data.get('intereses', 'No especificados')}

Por favor, proporciona:
1. Una evaluación general del progreso
2. Áreas recomendadas de enfoque
3. Estrategias educativas específicas
4. Actividades recomendadas
5. Próximos pasos sugeridos
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            raise Exception(f"Error al generar recomendación: {str(e)}")
    
    async def analyze_behavior(self, descripcion_comportamiento: str) -> str:
        """Analiza un comportamiento del niño"""
        if not self.is_configured:
            raise ValueError("Servicio Gemini no está configurado")
            
        try:
            prompt = f"""
Analiza el siguiente comportamiento observado en un niño con autismo:

{descripcion_comportamiento}

Por favor, proporciona:
1. Interpretación del comportamiento
2. Posibles desencadenantes
3. Estrategias de manejo
4. Cuándo buscar ayuda profesional
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            raise Exception(f"Error al analizar comportamiento: {str(e)}")
    
    async def generate_content(self, prompt: str) -> str:
        """Método genérico para generar contenido"""
        if not self.is_configured:
            raise ValueError("Servicio Gemini no está configurado")
            
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error al generar contenido: {str(e)}")


# Instanciar el servicio
gemini_service = GeminiService()

# Verificar que gemini_chat_service esté disponible
if not gemini_chat_service.is_configured:
    print("⚠ GeminiChatService no está configurado correctamente")

