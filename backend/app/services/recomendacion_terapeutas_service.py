# app/services/recomendaciones_service.py

from typing import List, Dict
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.personal import Personal
from app.models.terapia import Terapia, AsignacionTerapia
from app.models.nino import Nino
from app.models.recurso_terapeuta import RecursoTerapeuta
from app.models.tarea_asignada import TareaAsignada
from app.services.topsis_service import topsis


# ======================================================
# AFINIDAD PERSONAL - TERAPIA
# ======================================================
def _afinidad_terapia(personal: Personal, terapia: Terapia) -> float:
    """
    Heurística de afinidad entre un terapeuta y una terapia:
    - 1.0 si la terapia es su terapia principal
    - 0.8 si la terapia coincide con su especialidad principal
    - 0.5 en otros casos
    """
    if personal.id_terapia_principal == terapia.id_terapia:
        return 1.0

    nombre_terapia = (terapia.nombre or "").lower()
    especialidad = (personal.especialidad_principal or "").lower()
    if nombre_terapia and nombre_terapia in especialidad:
        return 0.8

    return 0.5


# ======================================================
# RECOMENDACIÓN DE TERAPEUTAS PARA UNA TERAPIA
# ======================================================
def recomendar_terapeutas_para_terapia(
    db: Session,
    id_terapia: int,
    pesos: Dict[str, float],
    max_resultados: int = 5,
) -> List[Dict]:
    """
    Recomendación de terapeutas para una terapia usando heurística + TOPSIS.
    Criterios considerados:
        - carga de pacientes (costo)
        - sesiones por semana (costo)
        - rating del terapeuta (beneficio)
        - afinidad con la terapia (beneficio)
    """
    terapia = db.query(Terapia).filter(Terapia.id_terapia == id_terapia).first()
    if not terapia:
        return []

    # Selección de personal activo asignado a la terapia
    personal_lista: List[Personal] = (
        db.query(Personal)
        .join(AsignacionTerapia, AsignacionTerapia.id_personal == Personal.id_personal)
        .filter(
            AsignacionTerapia.id_terapia == id_terapia,
            Personal.estado_laboral == "ACTIVO",
        )
        .all()
    )

    if not personal_lista:
        return []

    matriz: List[Dict[str, float]] = []
    meta: List[Personal] = []

    for p in personal_lista:
        carga = float(p.total_pacientes or 0)
        sesiones = float(p.sesiones_semana or 0)
        rating = float(p.rating or 0.0)
        afinidad = _afinidad_terapia(p, terapia)

        matriz.append({
            "carga": carga,
            "sesiones": sesiones,
            "rating": rating,
            "afinidad": afinidad,
        })
        meta.append(p)

    tipos = {
        "carga": "costo",
        "sesiones": "costo",
        "rating": "beneficio",
        "afinidad": "beneficio",
    }

    scores = topsis(matriz, pesos, tipos)

    resultados = [
        {"personal": p, "criterios": m, "score": s}
        for p, m, s in zip(meta, matriz, scores)
    ]

    # Ordenar de mayor a menor score
    resultados.sort(key=lambda x: x["score"], reverse=True)
    return resultados[:max_resultados]


# ======================================================
# RECOMENDACIÓN DE RECURSOS PARA UN NIÑO
# ======================================================
def _build_corpus(recursos: List[RecursoTerapeuta]) -> List[str]:
    """
    Construye un corpus de texto a partir de los recursos terapéuticos,
    combinando título, descripción, categoría y etiquetas.
    """
    corpus = []
    for r in recursos:
        texto = f"{r.titulo} {r.descripcion or ''} {r.categoria_nombre or ''} {' '.join(r.etiquetas or [])}"
        corpus.append(texto.lower())
    return corpus


def recomendar_recursos_para_nino(
    db: Session,
    id_nino: int,
    top_k: int = 5
) -> List[RecursoTerapeuta]:
    """
    Recomendación de recursos terapéuticos para un niño usando TF-IDF
    y similitud de coseno según su historial o diagnóstico principal.
    """
    nino = db.query(Nino).get(id_nino)
    if not nino:
        return []

    recursos = db.query(RecursoTerapeuta).filter(RecursoTerapeuta.estado == "ACTIVO").all()
    if not recursos:
        return []

    corpus = _build_corpus(recursos)

    # Historial de recursos utilizados por el niño
    tareas = (
        db.query(TareaAsignada)
        .filter(TareaAsignada.id_nino == id_nino, TareaAsignada.completado == True)
        .all()
    )

    historial_texto = ""
    for t in tareas:
        r = next((x for x in recursos if x.id == t.id_recurso), None)
        if r:
            historial_texto += f" {r.titulo} {r.descripcion or ''} {' '.join(r.etiquetas or [])}"

    # Si no hay historial, usar diagnóstico principal
    if not historial_texto and nino.diagnostico_principal:
        historial_texto = nino.diagnostico_principal

    # Si aún no hay referencia, devolver top_k primeros recursos
    if not historial_texto:
        return recursos[:top_k]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus + [historial_texto.lower()])

    perfil_vec = tfidf_matrix[-1]  # Última fila = perfil del niño
    recursos_vecs = tfidf_matrix[:-1]

    sims = cosine_similarity(perfil_vec, recursos_vecs)[0]

    # Ordenar por similitud descendente
    indices_ordenados = sims.argsort()[::-1]
    return [recursos[idx] for idx in indices_ordenados[:top_k]]
