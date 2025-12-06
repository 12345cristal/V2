import os
import requests
from fastapi import HTTPException

IA_SERVICE_URL = os.getenv("IA_SERVICE_URL", "http://localhost:8100")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "super-clave-interna")


def ia_resumen_sesion(texto: str) -> str:
    url = f"{IA_SERVICE_URL}/ia/resumen-sesion"
    r = requests.post(
        url,
        json={"texto": texto},
        headers={"X-Internal-Key": INTERNAL_API_KEY},
        timeout=30,
    )
    if r.status_code != 200:
        raise HTTPException(500, f"Error IA resumen: {r.text}")
    return r.json()["resumen"]


def ia_recomendaciones(recursos: list, perfil_nino: str):
    url = f"{IA_SERVICE_URL}/ia/recomendaciones"
    r = requests.post(
        url,
        json={"recursos": recursos, "perfil_nino": perfil_nino},
        headers={"X-Internal-Key": INTERNAL_API_KEY},
        timeout=30,
    )
    if r.status_code != 200:
        raise HTTPException(500, f"Error IA recomendacion: {r.text}")
    return r.json()
