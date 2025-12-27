"""
LEGACY: Mantiene compatibilidad hacia atrás con módulos existentes.
Para nuevo código, usa:
  - gemini_chat_service: chat terapéutico
  - gemini_embedding_service: embeddings y similitud
"""

from __future__ import annotations

from typing import List, Dict

# Imports reexportados para compatibilidad
from app.services.gemini_chat_service import (
    GeminiChatService,
    gemini_chat_service,
)
from app.services.gemini_embedding_service import (
    GeminiEmbeddingService,
    gemini_embedding_service,
)
from app.services.conversation_store import ConversationStore


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
        self.chat_service = gemini_chat_service
        self.embedding_service = gemini_embedding_service
        self.store = ConversationStore()
        self.configured = (
            self.chat_service.configured
            or self.embedding_service.configured
        )

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


# Singletons (compatibilidad)
gemini_service = GeminiService()

