from fastapi import APIRouter, Depends, Header, HTTPException
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ..core.config import settings

router = APIRouter(tags=["Recomendacion"])


def validar_internal_key(x_internal_key: str = Header(...)):
    if x_internal_key != settings.INTERNAL_API_KEY:
        raise HTTPException(403, "No autorizado")


@router.post("/recomendaciones")
def recomendar_recursos(payload: dict, _=Depends(validar_internal_key)):
    """
    payload:
    {
      "recursos": [
        {"id": 1, "titulo": "...", "descripcion": "...", "etiquetas": ["lenguaje", "inicio"]},
        ...
      ],
      "perfil_nino": "frases clave sobre diagnóstico, objetivos, historial..."
    }
    """
    recursos: List[Dict] = payload.get("recursos", [])
    perfil_nino: str = payload.get("perfil_nino", "")

    if not recursos:
        return []

    corpus = []
    for r in recursos:
        texto = " ".join([
            r.get("titulo", ""),
            r.get("descripcion", ""),
            " ".join(r.get("etiquetas", []))
        ])
        corpus.append(texto)

    corpus.append(perfil_nino)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)

    # último es el perfil del niño
    perfil_vec = X[-1]
    recursos_vec = X[:-1]

    sims = cosine_similarity(perfil_vec, recursos_vec)[0]

    resultados = []
    for rec, score in zip(recursos, sims):
        resultados.append({
            "id": rec["id"],
            "titulo": rec["titulo"],
            "score": float(score),
        })

    resultados.sort(key=lambda x: x["score"], reverse=True)
    return resultados[:10]
