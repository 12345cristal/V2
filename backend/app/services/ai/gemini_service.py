# app/services/ai/gemini_service.py
from google import genai
from google.genai import types
from app.core.config import settings
import json
import time


class GeminiClient:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("Gemini API Key no configurada en .env")

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
            http_options=types.HttpOptions(api_version="v1"),
        )
        self.model = settings.GEMINI_MODEL_ID

    # ------------------------------
    # IA: RESUMEN DE SESIÓN
    # ------------------------------
    def resumen_sesion(self, texto: str) -> str:
        prompt = f"""
        Eres un asistente terapéutico profesional del autismo.

        Resume la siguiente sesión de terapia en máximo **6 puntos claros**:

        • Avances observados  
        • Dificultades  
        • Comportamientos relevantes  
        • Recomendaciones para casa  
        • Indicadores de alerta (si hay)

        Texto de sesión:
        {texto}

        Responde en español, formato limpio.
        """

        resp = self.client.models.generate_content(
            model=self.model,
            contents=[prompt]
        )

        return resp.text

    # ------------------------------
    # IA: NOTAS CLÍNICAS TIPO SOAP
    # ------------------------------
    def generar_nota_SOAP(self, texto_sesion: str) -> str:
        prompt = f"""
        Genera una nota SOAP profesional basada en esta sesión:

        {texto_sesion}

        Formato:

        S: 
        O:
        A:
        P:

        - Escribe en tono clínico.
        - En español.
        """

        resp = self.client.models.generate_content(
            model=self.model,
            contents=[prompt]
        )
        return resp.text

    # ------------------------------
    # IA: ANALISIS EMOCIONAL DEL NIÑO
    # ------------------------------
    def perfil_emocional(self, texto: str) -> str:
        prompt = f"""
        Analiza el siguiente texto (de un terapeuta o tutor) y genera:

        • Nivel de ansiedad (bajo/medio/alto)  
        • Estímulos que detonan estrés  
        • Actividades calmantes sugeridas  
        • Riesgos a considerar  
        • Recomendaciones prácticas para el terapeuta  

        Texto:
        {texto}

        Responde en español.
        """

        resp = self.client.models.generate_content(
            model=self.model,
            contents=[prompt]
        )
        return resp.text

    # ------------------------------
    # IA: RECOMENDACIÓN DE TERAPIAS
    # ------------------------------
    def recomendar_terapias(self, diagnostico: str) -> str:
        prompt = f"""
        Basado en este diagnóstico de un niño:

        "{diagnostico}"

        Recomienda:
        • 3 terapias principales
        • 3 metas a corto plazo
        • Qué tipo de especialista debería atenderlo
        • Indicadores de progreso

        Responde en español.
        """

        resp = self.client.models.generate_content(
            model=self.model,
            contents=[prompt]
        )
        return resp.text

    # ------------------------------
    # IA: RECOMENDACIÓN DE ACTIVIDADES
    # ------------------------------
    def recomendar_actividades(self, perfil: str) -> str:
        prompt = f"""
        El siguiente es el perfil de un niño, incluyendo edad, diagnóstico y observaciones:
        {perfil}

        Genera una lista de 5 actividades terapéuticas:
        • Nombre  
        • Objetivo terapéutico  
        • Materiales  
        • Nivel de dificultad  
        • Cómo aplicarla en casa  

        Responde en español.
        """

        resp = self.client.models.generate_content(
            model=self.model,
            contents=[prompt]
        )
        return resp.text

    # ------------------------------
    # IA: EXPLICAR PROGRESO A PADRES
    # ------------------------------
    def explicar_progreso(self, resumen: str) -> str:
        prompt = f"""
        Explica el progreso terapéutico de un niño a sus padres de forma clara,
        positiva y empática.

        Resumen clínico:
        {resumen}

        El mensaje debe ser:
        • Comprensible
        • Empático
        • Sin tecnicismos
        • En español
        """

        resp = self.client.models.generate_content(
            model=self.model,
            contents=[prompt]
        )
        return resp.text
