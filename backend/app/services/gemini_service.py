# app/services/gemini_service.py
"""
Servicio para integración con Google Gemini
Genera embeddings y explicaciones en lenguaje natural
"""
import os
from typing import List, Dict, Optional
from collections import deque
from uuid import uuid4
import time
import google.generativeai as genai
import numpy as np


class GeminiService:
    """
    Servicio para interactuar con Gemini API
    """
    
    def __init__(self):
        # Configurar API Key desde settings (lazy import para evitar circular dependency)
        from app.core.config import settings
        api_key = settings.GEMINI_API_KEY
        
        self.configured = False
        
        if not api_key or not api_key.strip():
            print("⚠ ADVERTENCIA: GEMINI_API_KEY no está configurada. El sistema funcionará con funcionalidad limitada.")
            self.embedding_model = None
            self.text_model = None
            return
        
        try:
            genai.configure(api_key=api_key)
            
            # Modelo para embeddings
            self.embedding_model = "models/embedding-001"
            
            # Modelo para generación de texto (actualizado a Gemini 1.5)
            self.text_model = genai.GenerativeModel('gemini-1.5-flash')
            
            self.configured = True
            print("✅ Gemini AI configurado correctamente con gemini-1.5-flash")
        except Exception as e:
            print(f"⚠ Error configurando Gemini: {e}")
            self.embedding_model = None
            self.text_model = None

        # Almacén de conversaciones en memoria (TTL)
        self.store = ConversationStore(ttl_seconds=1800)

class ConversationStore:
    """Almacén simple en memoria para historial de chat por sesión."""
    def __init__(self, ttl_seconds: int = 1800):
        self.ttl = ttl_seconds
        self.sessions: Dict[str, Dict] = {}

    def _cleanup(self):
        now = time.time()
        expirados = [sid for sid, data in self.sessions.items() if now - data.get("updated_at", now) > self.ttl]
        for sid in expirados:
            try:
                del self.sessions[sid]
            except KeyError:
                pass

    def new_session(self) -> str:
        self._cleanup()
        sid = uuid4().hex
        self.sessions[sid] = {"messages": deque(maxlen=50), "updated_at": time.time()}
        return sid

    def append(self, session_id: str, rol: str, texto: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = {"messages": deque(maxlen=50), "updated_at": time.time()}
        self.sessions[session_id]["messages"].append({"rol": rol, "texto": texto})
        self.sessions[session_id]["updated_at"] = time.time()
        self._cleanup()

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        self._cleanup()
        if session_id not in self.sessions:
            return []
        return list(self.sessions[session_id]["messages"])[:]
    
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
    
    def chatbot_consulta(self, mensaje: str, contexto: Optional[Dict] = None, historial: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Chatbot para consultas sobre autismo y terapias
        
        Args:
            mensaje: Pregunta del usuario
            contexto: Información adicional (perfil del niño, historial, etc)
            
        Returns:
            Respuesta del chatbot
        """
        if not self.configured:
            return (
                "El chatbot de IA no está configurado. Por ahora puedo darte pautas generales basadas en buenas prácticas: \n"
                "- Establece rutinas predecibles y usa apoyos visuales.\n"
                "- Refuerza conductas deseadas con elogios inmediatos.\n"
                "- Divide tareas en pasos simples y modela cada uno.\n"
                "- Comunicación clara y concreta; ofrece opciones limitadas.\n"
                "- Ante rabietas: calma, valida la emoción y ofrece un espacio tranquilo.\n\n"
                "Configura la GEMINI_API_KEY en el backend para respuestas personalizadas."
            )
        
        contexto_str = ""
        if contexto:
            import json
            contexto_str = f"\n\nContexto adicional:\n{json.dumps(contexto, indent=2, ensure_ascii=False)}"
        
        # Armar historial si viene del cliente
        historial_str = ""
        if historial:
            try:
                ultimos = historial[-10:]  # limitar a los últimos 10 mensajes
                lineas = []
                for msg in ultimos:
                    rol = msg.get("rol", "usuario")
                    texto = msg.get("texto", "")
                    etiqueta = "Usuario" if rol == "usuario" else "Asistente"
                    lineas.append(f"- {etiqueta}: {texto}")
                if lineas:
                    historial_str = "\n\nConversación previa:\n" + "\n".join(lineas)
            except Exception as _:
                historial_str = ""

        prompt = f"""
Eres un asistente virtual especializado en trastorno del espectro autista (TEA) y terapias infantiles.

Responde de manera clara, profesional y empática. Si la pregunta es sobre un niño específico, personaliza tu respuesta.

**Pregunta del usuario:** {mensaje}
{contexto_str}
{historial_str}

Proporciona una respuesta útil, práctica y basada en evidencia científica. Máximo 200 palabras.
"""
        
        try:
            response = self.text_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error en chatbot: {e}")
            # Fallback útil y no bloqueante cuando hay errores con la API
            return (
                "Puedo ayudarte con pautas generales: \n"
                "- Establece rutinas predecibles y usa apoyos visuales.\n"
                "- Refuerza conductas deseadas con elogios inmediatos.\n"
                "- Divide las tareas en pasos simples y modela cada uno.\n"
                "- Usa comunicación clara y concreta; ofrece opciones limitadas.\n"
                "- Ante rabietas: mantén la calma, valida la emoción y guía a un espacio tranquilo.\n\n"
                "Si puedes, especifica edad, intereses y objetivo terapéutico para recomendaciones más precisas."
            )
    
    def generar_actividades_personalizadas(
        self,
        nombre_nino: str,
        edad: int,
        diagnostico: str,
        nivel_autismo: str,
        intereses: Optional[str] = None,
        objetivos: Optional[str] = None,
        cantidad: int = 5
    ) -> List[Dict]:
        """
        Genera actividades terapéuticas personalizadas
        
        Args:
            nombre_nino: Nombre del niño
            edad: Edad en años
            diagnostico: Diagnóstico principal
            nivel_autismo: Nivel de TEA (Leve, Moderado, Severo)
            intereses: Intereses del niño
            objetivos: Objetivos terapéuticos
            cantidad: Número de actividades a generar
            
        Returns:
            Lista de actividades en formato dict
        """
        if not self.configured:
            return self._actividades_por_defecto()
        
        prompt = f"""
Eres un terapeuta especializado en autismo. Genera {cantidad} actividades terapéuticas personalizadas para:

**Niño:** {nombre_nino}
**Edad:** {edad} años
**Diagnóstico:** {diagnostico}
**Nivel de autismo:** {nivel_autismo}
**Intereses:** {intereses or 'No especificados'}
**Objetivos terapéuticos:** {objetivos or 'Mejorar habilidades sociales y comunicación'}

Para cada actividad, proporciona:
1. **Nombre** (breve, atractivo)
2. **Descripción** (detallada, paso a paso)
3. **Objetivo** (qué habilidad desarrolla)
4. **Duración estimada** (en minutos)
5. **Materiales necesarios**
6. **Nivel de dificultad** (Básico, Intermedio, Avanzado)
7. **Área de desarrollo** (Comunicación, Social, Motora, Cognitiva, Sensorial)

Responde SOLO con un JSON válido, sin texto adicional:
[
  {{
    "nombre": "Nombre de la actividad",
    "descripcion": "Descripción detallada paso a paso",
    "objetivo": "Objetivo específico",
    "duracion_minutos": 30,
    "materiales": ["material1", "material2"],
    "nivel_dificultad": "Básico",
    "area_desarrollo": "Social"
  }}
]
"""
        
        try:
            import json
            response = self.text_model.generate_content(prompt)
            text = response.text.strip()
            
            # Limpiar markdown si viene envuelto
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            actividades = json.loads(text.strip())
            print(f"✅ Generadas {len(actividades)} actividades personalizadas con Gemini")
            return actividades
            
        except Exception as e:
            print(f"Error generando actividades: {e}")
            return self._actividades_por_defecto()
    
    def generar_plan_terapeutico(
        self,
        nombre_nino: str,
        edad: int,
        diagnostico: str,
        evaluacion_inicial: str,
        objetivos_padres: Optional[str] = None
    ) -> Dict:
        """
        Genera un plan terapéutico completo de 3 meses
        """
        if not self.configured:
            return self._plan_por_defecto()
        
        prompt = f"""
Eres un coordinador de terapias especializadas en autismo. Crea un plan terapéutico de 3 meses para:

**Niño:** {nombre_nino}, {edad} años
**Diagnóstico:** {diagnostico}
**Evaluación inicial:** {evaluacion_inicial}
**Objetivos de los padres:** {objetivos_padres or 'No especificados'}

Genera un plan estructurado con:
1. Objetivos generales (3-5 objetivos SMART)
2. Áreas de enfoque (priorizadas)
3. Frecuencia de sesiones recomendada
4. Terapias recomendadas (con justificación)
5. Indicadores de progreso (cómo medir avances)
6. Recomendaciones para padres

Responde SOLO con JSON válido:
{{
  "objetivos_generales": ["objetivo1", "objetivo2"],
  "areas_enfoque": ["area1", "area2"],
  "frecuencia_sesiones": "3 veces por semana",
  "terapias_recomendadas": [
    {{"tipo": "Terapia de Lenguaje", "justificacion": "Justificación"}}
  ],
  "indicadores_progreso": ["indicador1", "indicador2"],
  "recomendaciones_padres": ["recomendación1", "recomendación2"]
}}
"""
        
        try:
            import json
            response = self.text_model.generate_content(prompt)
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            plan = json.loads(text.strip())
            print(f"✅ Plan terapéutico generado con Gemini")
            return plan
            
        except Exception as e:
            print(f"Error generando plan: {e}")
            return self._plan_por_defecto()
    
    def analizar_progreso(
        self,
        nombre_nino: str,
        evaluaciones: List[Dict],
        periodo: str = "últimos 3 meses"
    ) -> Dict:
        """
        Analiza el progreso del niño basado en evaluaciones
        """
        if not self.configured:
            return {"error": "Gemini no configurado", "resumen": "Análisis no disponible"}
        
        import json
        
        prompt = f"""
Analiza el progreso terapéutico de {nombre_nino} en el {periodo}.

Evaluaciones:
{json.dumps(evaluaciones, indent=2, ensure_ascii=False)}

Genera un análisis que incluya:
1. Resumen del progreso
2. Áreas de mejora (avances destacados)
3. Áreas de oportunidad (necesitan más trabajo)
4. Tendencias observadas
5. Recomendaciones de ajuste
6. Próximos objetivos sugeridos
7. Calificación del progreso (0-10)

Responde SOLO con JSON:
{{
  "resumen": "Descripción general",
  "areas_mejora": ["area1", "area2"],
  "areas_oportunidad": ["area1", "area2"],
  "tendencias": ["tendencia1", "tendencia2"],
  "recomendaciones_ajuste": ["ajuste1"],
  "proximos_objetivos": ["objetivo1"],
  "calificacion_progreso": 8.0
}}
"""
        
        try:
            response = self.text_model.generate_content(prompt)
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            analisis = json.loads(text.strip())
            print(f"✅ Análisis de progreso generado")
            return analisis
            
        except Exception as e:
            print(f"Error analizando progreso: {e}")
            return {"error": str(e), "resumen": "Error en análisis"}
    
    def _actividades_por_defecto(self) -> List[Dict]:
        """Actividades por defecto cuando Gemini no está disponible"""
        return [
            {
                "nombre": "Juego de imitación",
                "descripcion": "Actividad para desarrollar habilidades sociales mediante imitación de gestos y expresiones faciales. El terapeuta realiza gestos simples y el niño los imita.",
                "objetivo": "Mejorar la comunicación no verbal y habilidades de imitación",
                "duracion_minutos": 20,
                "materiales": ["Espejo", "Imágenes de emociones", "Tarjetas visuales"],
                "nivel_dificultad": "Básico",
                "area_desarrollo": "Social"
            },
            {
                "nombre": "Rutina sensorial",
                "descripcion": "Actividades táctiles con diferentes texturas para estimulación sensorial controlada. Incluye exploración de materiales variados.",
                "objetivo": "Regular procesamiento sensorial y reducir hipersensibilidad",
                "duracion_minutos": 30,
                "materiales": ["Plastilina", "Arena kinética", "Pelotas texturizadas", "Telas suaves"],
                "nivel_dificultad": "Básico",
                "area_desarrollo": "Sensorial"
            },
            {
                "nombre": "Construcción con bloques",
                "descripcion": "Actividad de construcción guiada que promueve la planificación motora y seguimiento de instrucciones.",
                "objetivo": "Desarrollar habilidades motoras finas y planificación secuencial",
                "duracion_minutos": 25,
                "materiales": ["Bloques de construcción", "Imágenes de referencia", "Contenedor organizador"],
                "nivel_dificultad": "Intermedio",
                "area_desarrollo": "Motora"
            }
        ]
    
    def _plan_por_defecto(self) -> Dict:
        """Plan terapéutico por defecto"""
        return {
            "objetivos_generales": [
                "Mejorar habilidades de comunicación verbal y no verbal",
                "Desarrollar mayor interacción social con pares",
                "Fortalecer capacidades de autorregulación emocional"
            ],
            "areas_enfoque": ["Comunicación", "Social", "Sensorial", "Emocional"],
            "frecuencia_sesiones": "2-3 veces por semana (sesiones de 45-60 minutos)",
            "terapias_recomendadas": [
                {"tipo": "Terapia de Lenguaje", "justificacion": "Mejorar comunicación expresiva y receptiva"},
                {"tipo": "Terapia Ocupacional", "justificacion": "Trabajar integración sensorial y habilidades motoras"},
                {"tipo": "Terapia Conductual (ABA)", "justificacion": "Desarrollar habilidades sociales y reducir conductas desafiantes"}
            ],
            "indicadores_progreso": [
                "Aumento en palabras expresadas por sesión",
                "Mejora en contacto visual sostenido",
                "Reducción de episodios de desregulación",
                "Mayor tiempo de atención en actividades estructuradas"
            ],
            "recomendaciones_padres": [
                "Practicar actividades de comunicación en casa diariamente",
                "Mantener rutinas consistentes y predecibles",
                "Reforzar positivamente logros pequeños",
                "Crear un ambiente sensorial adecuado en el hogar"
            ]
        }


# Instancia singleton
gemini_service = GeminiService()
