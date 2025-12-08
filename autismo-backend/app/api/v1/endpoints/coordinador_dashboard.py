# app/api/v1/endpoints/coordinador_dashboard.py
"""
Endpoints del Dashboard del Coordinador
"""

from datetime import date, datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Float

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.models.usuario import Usuario
from app.models.nino import Nino
from app.models.personal import Personal
from app.models.terapia import Terapia, TerapiaNino, Sesion
from app.models.cita import Cita

router = APIRouter(
    prefix="/coordinador",
    tags=["Coordinador Dashboard"],
)


@router.get("/dashboard", response_model=Dict[str, Any])
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    """
    Obtener estadísticas del dashboard del coordinador.
    Retorna métricas clave del sistema de terapias.
    """

    # ==========================================
    # 1. Total de niños registrados
    # ==========================================
    total_ninos: int = db.query(func.count(Nino.id)).scalar() or 0

    # ==========================================
    # 2. Total de terapeutas (personal activo)
    #    Asumimos que "activo" viene desde Usuario.activo
    # ==========================================
    total_terapeutas: int = (
        db.query(func.count(Personal.id))
        .join(Usuario, Usuario.id == Personal.usuario_id)
        .filter(Usuario.activo == 1)
        .scalar()
        or 0
    )

    # ==========================================
    # 3. Total de terapias activas
    #    Asumimos campo Terapia.activo (TINYINT 0/1)
    # ==========================================
    total_terapias_activas: int = (
        db.query(func.count(Terapia.id))
        .filter(Terapia.activo == 1)
        .scalar()
        or 0
    )

    # ==========================================
    # 4. Citas de hoy
    #    Tu tabla CITAS maneja "fecha" y no "fecha_hora"
    # ==========================================
    hoy: date = date.today()

    total_citas_hoy: int = (
        db.query(func.count(Cita.id))
        .filter(Cita.fecha == hoy)
        .scalar()
        or 0
    )

    # ==========================================
    # 5. Citas pendientes
    #    Asumimos "estado_id" con algún ID para PENDIENTE (ej: 1)
    #    Si tienes catálogo cat_estado_cita, ajusta el ID.
    # ==========================================
    ESTADO_PENDIENTE_ID = 1  # Ajusta según tu catálogo real

    citas_pendientes: int = (
        db.query(func.count(Cita.id))
        .filter(Cita.estado_id == ESTADO_PENDIENTE_ID)
        .scalar()
        or 0
    )

    # ==========================================
    # 6. Progreso promedio de sesiones (0-100)
    # ==========================================
    progreso_promedio_raw = (
        db.query(func.avg(cast(Sesion.progreso, Float)))
        .filter(Sesion.progreso.isnot(None))
        .scalar()
    )

    progreso_promedio: float = (
        round(float(progreso_promedio_raw), 2) if progreso_promedio_raw else 0.0
    )

    # ==========================================
    # 7. Terapias más demandadas (top 5)
    # ==========================================
    terapias_mas_demandadas_query = (
        db.query(
            Terapia.nombre.label("nombre"),
            func.count(TerapiaNino.id).label("total_asignaciones"),
        )
        .join(TerapiaNino, TerapiaNino.terapia_id == Terapia.id)
        .group_by(Terapia.id, Terapia.nombre)
        .order_by(func.count(TerapiaNino.id).desc())
        .limit(5)
        .all()
    )

    terapias_mas_demandadas: List[Dict[str, Any]] = [
        {
            "nombre": row.nombre,
            "total_asignaciones": int(row.total_asignaciones),
        }
        for row in terapias_mas_demandadas_query
    ]

    # ==========================================
    # 8. Terapeutas con más pacientes (top 5)
    #    Contamos niños distintos por terapeuta
    # ==========================================
    terapeutas_con_mas_pacientes_query = (
        db.query(
            Personal.nombres.label("nombres"),
            Personal.apellido_paterno.label("apellido_paterno"),
            func.count(func.distinct(TerapiaNino.nino_id)).label("total_pacientes"),
        )
        .join(TerapiaNino, TerapiaNino.terapeuta_id == Personal.id)
        .group_by(Personal.id, Personal.nombres, Personal.apellido_paterno)
        .order_by(func.count(func.distinct(TerapiaNino.nino_id)).desc())
        .limit(5)
        .all()
    )

    terapeutas_con_mas_pacientes: List[Dict[str, Any]] = [
        {
            "nombre_completo": f"{row.nombres} {row.apellido_paterno}",
            "total_pacientes": int(row.total_pacientes),
        }
        for row in terapeutas_con_mas_pacientes_query
    ]

    # ==========================================
    # 9. Niños nuevos este mes
    #    Asumimos que Nino.fecha_registro existe
    # ==========================================
    primer_dia_mes = datetime(hoy.year, hoy.month, 1)

    ninos_nuevos_mes: int = (
        db.query(func.count(Nino.id))
        .filter(Nino.fecha_registro >= primer_dia_mes)
        .scalar()
        or 0
    )

    # ==========================================
    # 10. Estadísticas adicionales
    #     - total_sesiones
    #     - tasa_asistencia (%)
    # ==========================================
    total_sesiones: int = db.query(func.count(Sesion.id)).scalar() or 0

    sesiones_asistidas: int = (
        db.query(func.count(Sesion.id))
        .filter(Sesion.asistio == 1)
        .scalar()
        or 0
    )

    tasa_asistencia: float = (
        round((sesiones_asistidas / total_sesiones * 100), 2)
        if total_sesiones > 0
        else 0.0
    )

    # ==========================================
    # RESPUESTA FINAL
    # ==========================================
    return {
        "total_ninos": total_ninos,
        "total_terapeutas": total_terapeutas,
        "total_terapias_activas": total_terapias_activas,
        "total_citas_hoy": total_citas_hoy,
        "citas_pendientes": citas_pendientes,
        "progreso_promedio": progreso_promedio,
        "ninos_nuevos_mes": ninos_nuevos_mes,
        "total_sesiones": total_sesiones,
        "tasa_asistencia": tasa_asistencia,
        "terapias_mas_demandadas": terapias_mas_demandadas,
        "terapeutas_con_mas_pacientes": terapeutas_con_mas_pacientes,
        "fecha_consulta": hoy.isoformat(),
    }
