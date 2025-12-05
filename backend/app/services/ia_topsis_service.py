# app/services/ia_topsis_service.py
from sqlalchemy.orm import Session
from math import sqrt
from typing import List, Dict

from app.models.personal import Personal


def calcular_topsis_personal(db: Session) -> List[Dict]:
    """
    Calcula un score TOPSIS para personal usando:
    - total_pacientes (criterio de costo)
    - sesiones_semana (criterio de costo)
    - rating (criterio de beneficio)

    Devuelve:
    [
      {
        "id_personal": 1,
        "nombre_completo": "X",
        "score": 0.78
      },
      ...
    ]
    """
    q = (
        db.query(
            Personal.id_personal,
            Personal.nombres,
            Personal.apellido_paterno,
            Personal.apellido_materno,
            Personal.total_pacientes,
            Personal.sesiones_semana,
            Personal.rating,
        )
        .all()
    )

    datos = []
    for row in q:
        # evita Nones
        tp = row.total_pacientes or 0
        ss = row.sesiones_semana or 0
        rt = row.rating or 0
        datos.append(
            {
                "id_personal": row.id_personal,
                "nombre_completo": f"{row.nombres} {row.apellido_paterno} {row.apellido_materno or ''}".strip(),
                "tp": tp,
                "ss": ss,
                "rt": rt,
            }
        )

    if not datos:
        return []

    # Matriz de decisión
    tp_vals = [d["tp"] for d in datos]
    ss_vals = [d["ss"] for d in datos]
    rt_vals = [d["rt"] for d in datos]

    # Normalización vectorial
    def normalizar(vals):
        denom = sqrt(sum(v * v for v in vals)) or 1
        return [v / denom for v in vals]

    n_tp = normalizar(tp_vals)
    n_ss = normalizar(ss_vals)
    n_rt = normalizar(rt_vals)

    # Pesos (ajusta según importancia)
    w_tp, w_ss, w_rt = 0.4, 0.3, 0.3

    # Criterios costo/beneficio
    # costo: queremos MENOS total_pacientes y MENOS sesiones_semana
    # beneficio: queremos MÁS rating
    # Ideal positivo (mejor):
    v_tp_plus = min(n_tp)  # menos carga
    v_ss_plus = min(n_ss)
    v_rt_plus = max(n_rt)
    # Ideal negativo (peor):
    v_tp_minus = max(n_tp)
    v_ss_minus = max(n_ss)
    v_rt_minus = min(n_rt)

    resultados = []
    for i, d in enumerate(datos):
        # ponderados
        v_tp_i = n_tp[i] * w_tp
        v_ss_i = n_ss[i] * w_ss
        v_rt_i = n_rt[i] * w_rt

        # distancia a ideal positivo
        d_plus = sqrt(
            (v_tp_i - v_tp_plus * w_tp) ** 2 +
            (v_ss_i - v_ss_plus * w_ss) ** 2 +
            (v_rt_i - v_rt_plus * w_rt) ** 2
        )
        # distancia a ideal negativo
        d_minus = sqrt(
            (v_tp_i - v_tp_minus * w_tp) ** 2 +
            (v_ss_i - v_ss_minus * w_ss) ** 2 +
            (v_rt_i - v_rt_minus * w_rt) ** 2
        )
        score = d_minus / (d_plus + d_minus) if d_plus + d_minus != 0 else 0

        resultados.append(
            {
                "id_personal": d["id_personal"],
                "nombre_completo": d["nombre_completo"],
                "score": round(score, 4),
            }
        )

    # Ordenar desc
    resultados.sort(key=lambda x: x["score"], reverse=True)
    return resultados
