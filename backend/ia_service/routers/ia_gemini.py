from fastapi import APIRouter, Depends, Header, HTTPException
import requests

from ..core.config import settings

router = APIRouter(tags=["Gemini"])

GEMINI_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"


def validar_internal_key(x_internal_key: str = Header(...)):
    if x_internal_key != settings.INTERNAL_API_KEY:
        raise HTTPException(403, "No autorizado")


@router.post("/resumen-sesion")
def generar_resumen_sesion(payload: dict, _=Depends(validar_internal_key)):
    """
    payload esperado: { "texto": "bitácora completa..." }
    """
    texto = payload.get("texto")
    if not texto:
        raise HTTPException(400, "Falta 'texto'")

    prompt = (
        "Eres un asistente clínico. Resume la siguiente bitácora de sesión con un tono "
        "profesional, en lenguaje claro para padres y terapeutas, en máximo 5 líneas. "
        "Texto:\n" + texto
    )

    body = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    params = {"key": settings.GEMINI_API_KEY}
    r = requests.post(GEMINI_URL, params=params, json=body, timeout=30)

    if r.status_code != 200:
        raise HTTPException(500, f"Error en IA: {r.text}")

    data = r.json()
    resumen = data["candidates"][0]["content"]["parts"][0]["text"]

    return {"resumen": resumen}
