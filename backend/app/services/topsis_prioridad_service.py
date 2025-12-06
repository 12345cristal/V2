from typing import List, Dict
from sqlalchemy.orm import Session

from app.models.nino import Nino
from app.models.cita import Cita

from app.services.topsis_service import topsis


def calcular_prioridad_ninos(
    db: Session,
    pesos: Dict[str, float],
    max_resultados: int = 10,
):
    ninos: List[Nino] = db.query(Nino).all()
    matriz = []
    meta = []

    for n in ninos:
        # tiempo desde su última sesión
        citas = (
            db.query(Cita)
            .filter(Cita.id_nino == n.id_nino)
            .order_by(Cita.fecha.desc())
            .all()
        )

        if citas:
            ultima_fecha = citas[0].fecha
            dias_sin_sesion = (date.today() - ultima_fecha).days
            asistencias = sum(1 for c in citas if c.estado == "ASISTIO")
            inasistencias = sum(1 for c in citas if c.estado == "NO_ASISTIO")
        else:
            dias_sin_sesion = 30
            asistencias = 0
            inasistencias = 0

        prioridad_clinica = 1.0  # valor asignado por el coordinador (puede venir de la BD)

        matriz.append({
            "prioridad": prioridad_clinica,
            "dias_sin_sesion": dias_sin_sesion,
            "asistencias": asistencias,
            "inasistencias": inasistencias,
        })
        meta.append(n)

    tipos = {
        "prioridad": "beneficio",
        "dias_sin_sesion": "beneficio",
        "asistencias": "beneficio",
        "inasistencias": "costo",
    }

    scores = topsis(matriz, pesos, tipos)

    resultados = []
    for n, m, s in zip(meta, matriz, scores):
        resultados.append({
            "nino": n,
            "criterios": m,
            "score": s,
        })

    resultados.sort(key=lambda x: x["score"], reverse=True)
    return resultados[:max_resultados]
