# app/services/ai/ninos_ai_service.py
from sqlalchemy.orm import Session
from typing import Tuple
import numpy as np

from app.models.nino import Nino
from app.models.terapia import SesionTerapia, TerapiaNino  # crea estos models cuando hagamos módulo terapias


def calcular_progreso_y_riesgo(db: Session, nino_id: int) -> Tuple[float, float]:
    """
    Devuelve (progreso_general [0-100], riesgo [0-1])
    Progreso: promedio de nivel_progreso de sesiones.
    Riesgo: TOPSIS simple con #terapias, #sesiones, asistencia.
    """

    # Obtener sesiones
    q = (
        db.query(SesionTerapia)
        .join(TerapiaNino, SesionTerapia.terapia_nino_id == TerapiaNino.id)
        .filter(TerapiaNino.nino_id == nino_id)
    )
    sesiones = q.all()

    if not sesiones:
        # sin sesiones => progreso 0, riesgo medio
        return 0.0, 0.5

    niveles = [s.nivel_progreso for s in sesiones if s.nivel_progreso is not None]
    if niveles:
        prog = float(sum(niveles) / len(niveles))
    else:
        prog = 0.0

    # TOPSIS muy básico
    total_terapias = (
        db.query(TerapiaNino).filter(TerapiaNino.nino_id == nino_id).count()
    )
    total_sesiones = len(sesiones)
    asistidas = sum(1 for s in sesiones if s.asistio)

    # construir vector
    matriz = np.array([[total_terapias, total_sesiones, asistidas]], dtype=float)
    pesos = np.array([0.4, 0.3, 0.3])
    ideal = matriz.max(axis=0)
    anti = matriz.min(axis=0)

    dist_ideal = np.linalg.norm(matriz - ideal)
    dist_anti = np.linalg.norm(matriz - anti)
    if dist_ideal + dist_anti == 0:
        riesgo = 0.5
    else:
        score = dist_anti / (dist_ideal + dist_anti)
        # interpretamos score bajo = mayor riesgo
        riesgo = float(1 - score)

    # normalizar progreso [0-100]
    if prog > 100:
        prog = 100.0
    if prog < 0:
        prog = 0.0

    return prog, riesgo
