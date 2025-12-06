# app/services/ia_gemini_service.py

import os
import httpx
from typing import Optional
from fastapi import HTTPException, status
from app.core.config import settings

# =============================================================
# CONFIGURACIÓN
# =============================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", settings.GEMINI_API_KEY)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", settings.GEMINI_MODEL or "gemini-1.5-flash")
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


# =============================================================
# FUNCIONES PRINCIPALES
# =============================================================
async def generar_resumen_sesion(texto_bitacora: str) -> str:
    """
    Llama a la API de Gemini para generar un resumen clínico breve de la sesión.
    Retorna un texto de 5-7 líneas en español, orientado a padres y equipo clínico.
    """

    # --- Fallback en desarrollo si no hay API KEY ---
    if not GEMINI_API_KEY:
        return (
            "Resumen IA (modo desarrollo): el niño mostró avances "
            "en atención, comunicación y regulación emocional."
        )

    # --- Construcción del prompt ---
    prompt = (
        "Eres un asistente clínico que resume sesiones de terapia para niños con TEA. "
        "Genera un resumen breve (máximo 5-7 líneas) en español claro, "
        "para coordinadores, terapeutas y padres, sin datos personales.\n\n"
        f"BITÁCORA:\n{texto_bitacora}"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 400,
        },
    }

    # --- Llamada a Gemini ---
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(GEMINI_ENDPOINT, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

            # --- Validación de respuesta ---
            candidates = data.get("candidates") or []
            if not candidates:
                return "No se pudo generar resumen IA (sin candidatos)."

            content = candidates[0].get("content", {})
            parts = content.get("parts") or []
            if not parts:
                return "No se pudo generar resumen IA (sin contenido)."

            texto_resumen = parts[0].get("text", "").strip()
            return texto_resumen or "No se pudo generar resumen IA (texto vacío)."

        except httpx.HTTPError as e:
            # En producción podrías loguear con logger
            return f"No se pudo generar resumen IA: {str(e)}"

