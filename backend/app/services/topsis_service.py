# app/services/topsis_service.py

from typing import List
import numpy as np


def topsis(
    matriz: List[List[float]],
    pesos: List[float],
    criterios_beneficio: List[bool],
) -> List[float]:
    """
    Implementación TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution).

    Parámetros:
        matriz: List[List[float]] -> m x n, filas=alternativas, columnas=criterios
        pesos: List[float] -> n, pesos de cada criterio (no necesariamente normalizados)
        criterios_beneficio: List[bool] -> n, True=beneficio, False=costo

    Retorna:
        List[float]: Score de cada alternativa (0 a 1), mayor = mejor.
    """

    # Convertir a array numpy
    m = np.array(matriz, dtype=float)
    pesos = np.array(pesos, dtype=float)

    if m.size == 0 or pesos.size == 0:
        return []

    # 1) Normalización por norma Euclídea (columna a columna)
    norm = np.linalg.norm(m, axis=0)
    norm[norm == 0] = 1.0
    m_norm = m / norm

    # 2) Aplicar pesos
    m_pond = m_norm * pesos

    # 3) Determinar ideal positivo y negativo
    ideal_pos = np.array([
        col.max() if beneficio else col.min()
        for col, beneficio in zip(m_pond.T, criterios_beneficio)
    ])
    ideal_neg = np.array([
        col.min() if beneficio else col.max()
        for col, beneficio in zip(m_pond.T, criterios_beneficio)
    ])

    # 4) Calcular distancias a los ideales
    dist_pos = np.linalg.norm(m_pond - ideal_pos, axis=1)
    dist_neg = np.linalg.norm(m_pond - ideal_neg, axis=1)

    # 5) Score TOPSIS
    scores = dist_neg / (dist_pos + dist_neg + 1e-12)  # evitar división por cero
    return scores.tolist()
