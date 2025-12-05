# app/services/ia_recomendacion_service.py

import math
from collections import Counter
from typing import List, Dict

from sqlalchemy.orm import Session

from app.models.recurso_terapeuta import RecursoTerapeuta
from app.models.tarea_recurso import TareaRecurso


def _tokenizar(texto: str) -> List[str]:
    texto = (texto or "").lower()
    # separar por espacios y quitar tokens muy cortos
    tokens = [t.strip(".,;:!?()[]{}\"'") for t in texto.split()]
    return [t for t in tokens if len(t) > 2]


def _construir_texto_recurso(r: RecursoTerapeuta) -> str:
    partes = [r.titulo or "", r.descripcion or ""]
    if r.etiquetas:
        partes.append(r.etiquetas.replace(",", " "))
    partes.append(r.categoria_id or "")
    partes.append(r.nivel_id or "")
    partes.append(r.tipo_id or "")
    return " ".join(partes)


def _tf_idf_vectors(docs: List[List[str]]) -> Dict[str, Dict[str, float]]:
    """
    docs: lista de documentos, cada doc es lista de tokens.
    retorno: dict[doc_index_str][term] = tfidf
    """
    N = len(docs)
    vocab = set()
    df = Counter()

    # build vocab and df
    for doc in docs:
        terms = set(doc)
        vocab.update(terms)
        for t in terms:
            df[t] += 1

    # compute idf
    idf = {}
    for t in vocab:
        idf[t] = math.log((N + 1) / (df[t] + 1)) + 1.0

    # compute tf-idf
    vectors: Dict[str, Dict[str, float]] = {}
    for i, doc in enumerate(docs):
        tf = Counter(doc)
        length = len(doc) or 1
        vec = {}
        for t, c in tf.items():
            vec[t] = (c / length) * idf[t]
        vectors[str(i)] = vec

    return vectors


def _cosine_sim(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    if not vec1 or not vec2:
        return 0.0

    # dot product
    common_terms = set(vec1.keys()) & set(vec2.keys())
    dot = sum(vec1[t] * vec2[t] for t in common_terms)

    # norms
    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)


def recomendar_recursos_para_nino(
    db: Session,
    id_nino: int,
    top_k: int = 5,
) -> List[RecursoTerapeuta]:
    """
    Genera recomendaciones de recursos para un niño usando
    TF-IDF + coseno sobre las descripciones/etiquetas.
    """

    # 1) Recursos que el niño ya ha utilizado/completado
    tareas = (
        db.query(TareaRecurso)
        .filter(TareaRecurso.nino_id == id_nino, TareaRecurso.completado == True)
        .all()
    )
    recursos_usados_ids = {t.recurso_id for t in tareas}

    if not recursos_usados_ids:
        # Si no tiene historial, devolvemos algunos recursos destacados/nuevos
        return (
            db.query(RecursoTerapeuta)
            .order_by(RecursoTerapeuta.es_destacado.desc(),
                      RecursoTerapeuta.es_nuevo.desc())
            .limit(top_k)
            .all()
        )

    recursos_usados = (
        db.query(RecursoTerapeuta)
        .filter(RecursoTerapeuta.id.in_(recursos_usados_ids))
        .all()
    )

    # 2) Recursos candidatos (no usados aún)
    candidatos = (
        db.query(RecursoTerapeuta)
        .filter(~RecursoTerapeuta.id.in_(recursos_usados_ids))
        .all()
    )

    if not candidatos:
        return []

    # 3) Construir "perfil" del niño: bag-of-words de todos los recursos usados
    tokens_perfil: List[str] = []
    for r in recursos_usados:
        tokens_perfil += _tokenizar(_construir_texto_recurso(r))

    # 4) Construir documentos: [perfil_niño, recurso_0, recurso_1, ... ]
    docs_tokens: List[List[str]] = [tokens_perfil]
    for r in candidatos:
        docs_tokens.append(_tokenizar(_construir_texto_recurso(r)))

    # 5) TF-IDF
    vectors = _tf_idf_vectors(docs_tokens)
    vec_perfil = vectors["0"]

    # 6) Similitud coseno entre perfil y cada recurso
    scores = []
    for idx, r in enumerate(candidatos, start=1):
        vec_recurso = vectors[str(idx)]
        sim = _cosine_sim(vec_perfil, vec_recurso)
        scores.append((r, sim))

    # 7) Ordenar por score y devolver top_k
    scores.sort(key=lambda x: x[1], reverse=True)
    recomendados = [r for (r, s) in scores if s > 0][:top_k]

    return recomendados
