# app/services/ai/topsis_service.py
import numpy as np


def calcular_prioridad_cita(duracion, edad, es_nuevo):
    # Matriz simple (puedes mejorarla)
    matriz = np.array([
        [duracion, edad, 1 if es_nuevo else 0]
    ], dtype=float)

    pesos = np.array([0.5, 0.3, 0.2])
    ideal = matriz.max(axis=0)
    anti = matriz.min(axis=0)

    dist_ideal = np.linalg.norm(matriz - ideal)
    dist_anti = np.linalg.norm(matriz - anti)

    score = dist_anti / (dist_ideal + dist_anti)
    return float(score)
