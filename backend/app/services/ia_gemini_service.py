# app/services/ia_gemini_service.py

import httpx
from typing import Optional
from app.core.config import settings


GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{settings.GEMINI_MODEL}:generateContent"
)


async def generar_resumen_sesion(texto_bitacora: str) -> str:
    """
    Llama a la API de Gemini para generar un resumen clínico breve.
    Ajusta el body EXACTO al formato oficial de Gemini que estés usando.
    """
    if not settings.GEMINI_API_KEY:
        # En desarrollo puedes devolver un mock
        return (
            "Resumen IA (modo desarrollo): el niño mostró avances "
            "en atención, comunicación y regulación emocional."
        )

    prompt = (
        "Eres un asistente clínico que ayuda a sintetizar notas de terapia "
        "para un centro de atención a niños con autismo.\n"
        "A partir del siguiente texto de bitácora, genera un resumen breve "
        "(5-7 líneas) en español, claro y orientado a los padres y al equipo clínico.\n\n"
        f"BITÁCORA:\n{texto_bitacora}"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": settings.GEMINI_API_KEY,
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 400,
        },
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(GEMINI_ENDPOINT, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

            # Ajusta según el formato real de la respuesta de Gemini
            # Aquí asumimos algo como data["candidates"][0]["content"]["parts"][0]["text"]
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
            # En producción podrías loguear
            return f"No se pudo generar resumen IA: {str(e)}"
