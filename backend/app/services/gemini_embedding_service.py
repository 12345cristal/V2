# app/services/gemini_embedding_service.py
import numpy as np
import google.generativeai as genai
from typing import List

from app.core.config import settings


class GeminiEmbeddingService:
    """
    Servicio de embeddings para similitud de contenidos.
    Usado en TOPSIS, recomendaciones y búsqueda semántica.
    """

    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        self.configured = False

        if not api_key:
            print("[WARN] Embeddings Gemini no configurados.")
            return

        try:
            genai.configure(api_key=api_key)
            self.model = "models/embedding-001"
            self.configured = True
            print("[OK] Gemini Embeddings listo")
        except Exception as e:
            print(f"[WARN] Error configurando embeddings: {e}")

    def embed(self, text: str) -> List[float]:
        """
        Genera embedding para un texto.
        
        Args:
            text: Texto a vectorizar
            
        Returns:
            Vector de 768 dimensiones
        """
        if not self.configured:
            return self._hash_embedding(text)

        try:
            res = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document",
            )
            return res["embedding"]
        except Exception as e:
            print(f"[WARN] Error generando embedding: {e}")
            return self._hash_embedding(text)

    def embed_perfil_nino(self, datos_nino: dict) -> tuple[List[float], str]:
        """
        Genera embedding del perfil de un niño.
        
        Args:
            datos_nino: Dict con datos del niño
            
        Returns:
            Tupla (embedding, texto_perfil)
        """
        texto = f"""
Perfil del niño: {datos_nino.get('nombre', '')}
Edad: {datos_nino.get('edad', '')} años
Diagnósticos: {', '.join(datos_nino.get('diagnosticos', []))}
Dificultades: {', '.join(datos_nino.get('dificultades', []))}
Fortalezas: {', '.join(datos_nino.get('fortalezas', []))}
Notas clínicas: {datos_nino.get('notas_clinicas', '')}
Sensibilidades: {', '.join(datos_nino.get('sensibilidades', []))}
Áreas prioritarias: {', '.join(datos_nino.get('areas_prioritarias', []))}
        """.strip()
        
        embedding = self.embed(texto)
        return embedding, texto

    def embed_actividad(self, datos_actividad: dict) -> tuple[List[float], str]:
        """
        Genera embedding de una actividad terapéutica.
        
        Args:
            datos_actividad: Dict con datos de actividad
            
        Returns:
            Tupla (embedding, texto_actividad)
        """
        texto = f"""
Actividad: {datos_actividad.get('nombre', '')}
Descripción: {datos_actividad.get('descripcion', '')}
Objetivo: {datos_actividad.get('objetivo', '')}
Área de desarrollo: {datos_actividad.get('area_desarrollo', '')}
Tags: {', '.join(datos_actividad.get('tags', []))}
Nivel de dificultad: {datos_actividad.get('dificultad', '')}
Materiales: {datos_actividad.get('materiales', '')}
        """.strip()
        
        embedding = self.embed(texto)
        return embedding, texto

    def similitud_coseno(
        self, vector1: List[float], vector2: List[float]
    ) -> float:
        """
        Calcula similitud coseno entre dos vectores.
        
        Args:
            vector1: Primer vector
            vector2: Segundo vector
            
        Returns:
            Similitud normalizada [0, 1]
        """
        try:
            v1 = np.array(vector1)
            v2 = np.array(vector2)
            dot = np.dot(v1, v2)
            mag1 = np.linalg.norm(v1)
            mag2 = np.linalg.norm(v2)
            
            if mag1 == 0 or mag2 == 0:
                return 0.0
            
            similitud = dot / (mag1 * mag2)
            return float((similitud + 1) / 2)  # Normalizar a [0, 1]
        except Exception as e:
            print(f"❌ Error en similitud: {e}")
            return 0.0

    @staticmethod
    def _hash_embedding(text: str) -> List[float]:
        """
        Fallback: genera embedding determinista basado en hash.
        Útil cuando Gemini API no está disponible.
        """
        import hashlib

        h = int(hashlib.md5(text.encode()).hexdigest(), 16)
        np.random.seed(h % (2**32))
        return np.random.rand(768).tolist()


# Singleton
gemini_embedding_service = GeminiEmbeddingService()
