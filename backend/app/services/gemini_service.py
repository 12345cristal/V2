# app/services/gemini_service.py
"""
Servicio para integración con Google Gemini
Genera embeddings y explicaciones en lenguaje natural
"""
import os
from typing import List, Dict, Optional
import google.generativeai as genai
import numpy as np


class GeminiService:
    """
    Servicio para interactuar con Gemini API
    """
    
    def __init__(self):
        # Configurar API Key desde variables de entorno
        api_key = os.getenv("GEMINI_API_KEY")
        
        self.configured = False
        
        if not api_key:
            print("⚠ ADVERTENCIA: GEMINI_API_KEY no está configurada. El sistema funcionará con funcionalidad limitada.")
            self.embedding_model = None
            self.text_model = None
            return
        
        try:
            genai.configure(api_key=api_key)
            
            # Modelo para embeddings
            self.embedding_model = "models/embedding-001"
            
            # Modelo para generación de texto
            self.text_model = genai.GenerativeModel('gemini-pro')
            
            self.configured = True
        except Exception as e:
            print(f"⚠ Error configurando Gemini: {e}")
            self.embedding_model = None
            self.text_model = None
    
    def generar_embedding(self, texto: str) -> List[float]:
        """
        Genera un embedding vectorial a partir de texto
        
        Args:
            texto: Texto para convertir a embedding
            
        Returns:
            Lista de floats representando el embedding
        """
        if not self.configured:
            # Generar un vector aleatorio pero consistente basado en hash del texto
            import hashlib
            hash_val = int(hashlib.md5(texto.encode()).hexdigest(), 16)
            np.random.seed(hash_val % (2**32))
            return np.random.rand(768).tolist()
        
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=texto,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generando embedding: {e}")
            # Retornar vector basado en hash
            import hashlib
            hash_val = int(hashlib.md5(texto.encode()).hexdigest(), 16)
            np.random.seed(hash_val % (2**32))
            return np.random.rand(768).tolist()
    
    def generar_embedding_perfil_nino(self, datos_nino: Dict) -> tuple[List[float], str]:
        """
        Genera embedding del perfil completo del niño
        
        Args:
            datos_nino: Diccionario con información del niño
            
        Returns:
            Tupla (embedding, texto_usado)
        """
        # Construir texto descriptivo del perfil
        texto_perfil = f"""
        Perfil del niño: {datos_nino.get('nombre', '')}
        Edad: {datos_nino.get('edad', '')} años
        Diagnósticos: {', '.join(datos_nino.get('diagnosticos', []))}
        Dificultades: {', '.join(datos_nino.get('dificultades', []))}
        Fortalezas: {', '.join(datos_nino.get('fortalezas', []))}
        Notas clínicas: {datos_nino.get('notas_clinicas', '')}
        Sensibilidades: {', '.join(datos_nino.get('sensibilidades', []))}
        Áreas de desarrollo prioritarias: {', '.join(datos_nino.get('areas_prioritarias', []))}
        """
        
        embedding = self.generar_embedding(texto_perfil.strip())
        return embedding, texto_perfil.strip()
    
    def generar_embedding_actividad(self, datos_actividad: Dict) -> tuple[List[float], str]:
        """
        Genera embedding de una actividad terapéutica
        
        Args:
            datos_actividad: Diccionario con información de la actividad
            
        Returns:
            Tupla (embedding, texto_usado)
        """
        texto_actividad = f"""
        Actividad: {datos_actividad.get('nombre', '')}
        Descripción: {datos_actividad.get('descripcion', '')}
        Objetivo: {datos_actividad.get('objetivo', '')}
        Área de desarrollo: {datos_actividad.get('area_desarrollo', '')}
        Tags: {', '.join(datos_actividad.get('tags', []))}
        Nivel de dificultad: {datos_actividad.get('dificultad', '')}
        Materiales: {datos_actividad.get('materiales', '')}
        """
        
        embedding = self.generar_embedding(texto_actividad.strip())
        return embedding, texto_actividad.strip()
    
    def calcular_similitud_coseno(self, vector1: List[float], vector2: List[float]) -> float:
        """
        Calcula similitud coseno entre dos vectores
        
        Args:
            vector1: Primer vector
            vector2: Segundo vector
            
        Returns:
            Score de similitud (0-1)
        """
        try:
            v1 = np.array(vector1)
            v2 = np.array(vector2)
            
            # Calcular producto punto y magnitudes
            dot_product = np.dot(v1, v2)
            magnitude1 = np.linalg.norm(v1)
            magnitude2 = np.linalg.norm(v2)
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            similitud = dot_product / (magnitude1 * magnitude2)
            
            # Normalizar a rango 0-1
            return float((similitud + 1) / 2)
        except Exception as e:
            print(f"Error calculando similitud: {e}")
            return 0.0
    
    def explicar_recomendacion_actividades(
        self,
        nombre_nino: str,
        perfil_nino: str,
        actividades_recomendadas: List[Dict],
        contexto_adicional: Optional[str] = None
    ) -> str:
        """
        Genera explicación en lenguaje natural de por qué se recomiendan ciertas actividades
        
        Args:
            nombre_nino: Nombre del niño
            perfil_nino: Descripción del perfil del niño
            actividades_recomendadas: Lista de actividades con scores
            contexto_adicional: Información adicional relevante
            
        Returns:
            Texto explicativo en lenguaje natural
        """
        prompt = f"""
        Eres un terapeuta experto que debe explicar de forma clara y profesional por qué se recomiendan ciertas actividades terapéuticas.
        
        PERFIL DEL NIÑO:
        {perfil_nino}
        
        ACTIVIDADES RECOMENDADAS:
        """
        
        for i, act in enumerate(actividades_recomendadas[:5], 1):
            prompt += f"\n{i}. {act['nombre']} - Score: {act['score']:.2f}"
            prompt += f"\n   Objetivo: {act.get('objetivo', '')}"
        
        if contexto_adicional:
            prompt += f"\n\nCONTEXTO ADICIONAL:\n{contexto_adicional}"
        
        prompt += """
        
        Genera una explicación profesional y empática que:
        1. Explique por qué estas actividades son adecuadas para el perfil del niño
        2. Destaque cómo abordan sus necesidades específicas
        3. Mencione qué áreas de desarrollo se trabajarán
        4. Sea comprensible tanto para terapeutas como para padres
        5. Sea concisa (máximo 150 palabras)
        """
        
        if not self.configured:
            return f"Estas actividades han sido seleccionadas basándose en el perfil de {nombre_nino}, considerando sus necesidades específicas de desarrollo y características individuales. Las actividades recomendadas buscan fortalecer las áreas que requieren apoyo mientras aprovechan sus fortalezas naturales."
        
        try:
            response = self.text_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generando explicación: {e}")
            return "Estas actividades han sido seleccionadas basándose en el perfil y necesidades específicas del niño."
    
    def explicar_seleccion_terapeuta(
        self,
        nombre_nino: str,
        terapia_tipo: str,
        terapeuta_seleccionado: Dict,
        criterios_topsis: Dict,
        ranking_top3: List[Dict]
    ) -> str:
        """
        Genera explicación de por qué se seleccionó un terapeuta específico usando TOPSIS
        
        Args:
            nombre_nino: Nombre del niño
            terapia_tipo: Tipo de terapia
            terapeuta_seleccionado: Datos del terapeuta seleccionado
            criterios_topsis: Criterios y pesos usados en TOPSIS
            ranking_top3: Top 3 terapeutas del ranking
            
        Returns:
            Explicación en lenguaje natural
        """
        prompt = f"""
        Eres un coordinador clínico que debe explicar por qué se seleccionó un terapeuta específico para un niño.
        
        CONTEXTO:
        - Niño: {nombre_nino}
        - Tipo de terapia: {terapia_tipo}
        
        TERAPEUTA SELECCIONADO:
        - Nombre: {terapeuta_seleccionado.get('nombre', '')}
        - Score TOPSIS: {terapeuta_seleccionado.get('score', 0):.3f}
        - Experiencia: {terapeuta_seleccionado.get('experiencia_anos', '')} años
        - Especialidad: {terapeuta_seleccionado.get('especialidad', '')}
        - Carga actual: {terapeuta_seleccionado.get('carga_trabajo', '')} pacientes
        
        CRITERIOS DE EVALUACIÓN (pesos usados):
        """
        
        for criterio, peso in criterios_topsis.items():
            prompt += f"\n- {criterio}: {peso*100:.1f}%"
        
        prompt += "\n\nTOP 3 CANDIDATOS:"
        for i, t in enumerate(ranking_top3[:3], 1):
            prompt += f"\n{i}. {t.get('nombre', '')} - Score: {t.get('score', 0):.3f}"
        
        prompt += """
        
        Genera una explicación profesional que:
        1. Justifique por qué este terapeuta es el más adecuado
        2. Destaque sus fortalezas relevantes
        3. Explique cómo los criterios influyeron en la decisión
        4. Sea clara y justificable clínicamente
        5. Sea concisa (máximo 120 palabras)
        """
        
        if not self.configured:
            return f"El terapeuta {terapeuta_seleccionado.get('nombre', '')} fue seleccionado mediante análisis multicriterio TOPSIS, considerando su experiencia de {terapeuta_seleccionado.get('experiencia_anos', 0)} años, disponibilidad y carga de trabajo óptima para atender las necesidades de {nombre_nino} en {terapia_tipo}."
        
        try:
            response = self.text_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generando explicación: {e}")
            return f"El terapeuta {terapeuta_seleccionado.get('nombre', '')} fue seleccionado por su experiencia y disponibilidad óptima."
    
    def generar_sugerencias_clinicas(
        self,
        perfil_nino: str,
        actividades_actuales: List[str],
        progreso_reciente: str
    ) -> str:
        """
        Genera sugerencias clínicas personalizadas
        
        Args:
            perfil_nino: Perfil del niño
            actividades_actuales: Actividades que se están usando
            progreso_reciente: Notas sobre progreso
            
        Returns:
            Sugerencias clínicas
        """
        prompt = f"""
        Eres un terapeuta experto en TEA y desarrollo infantil. Genera sugerencias clínicas breves y accionables.
        
        PERFIL:
        {perfil_nino}
        
        ACTIVIDADES ACTUALES:
        {', '.join(actividades_actuales)}
        
        PROGRESO RECIENTE:
        {progreso_reciente}
        
        Genera 3-4 sugerencias específicas y prácticas para:
        1. Optimizar actividades actuales
        2. Nuevas estrategias a considerar
        3. Ajustes basados en el progreso
        
        Sé conciso y específico (máximo 100 palabras).
        """
        
        if not self.configured:
            return "Continuar con el plan terapéutico actual, manteniendo las actividades que han mostrado buenos resultados. Monitorear el progreso semanalmente y ajustar la intensidad según la respuesta del niño. Considerar incorporar nuevas estrategias gradualmente."
        
        try:
            response = self.text_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generando sugerencias: {e}")
            return "Continuar con el plan actual y monitorear progreso semanalmente."


# Instancia singleton
gemini_service = GeminiService()
