"""
Endpoints del Dashboard del Coordinador
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, cast, Float
from datetime import datetime, date
from typing import Dict, Any, List

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.models.usuario import Usuario
from app.models.nino import Nino
from app.models.personal import Personal
from app.models.terapia import Terapia, TerapiaNino, Sesion
from app.models.cita import Cita

router = APIRouter(prefix="/coordinador", tags=["Coordinador Dashboard"])


@router.get("/dashboard", response_model=Dict[str, Any])
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtener estadísticas del dashboard del coordinador.
    Retorna métricas clave del sistema de terapias.
    """
    
    # ==========================================
    # 1. Total de niños registrados
    # ==========================================
    total_ninos = db.query(func.count(Nino.id)).scalar() or 0
    
    # ==========================================
    # 2. Total de terapeutas (personal activo)
    # ==========================================
    total_terapeutas = db.query(func.count(Personal.id)).filter(
        Personal.activo == 1
    ).scalar() or 0
    
    # ==========================================
    # 3. Total de terapias activas
    # ==========================================
    total_terapias_activas = db.query(func.count(Terapia.id)).filter(
        Terapia.activo == 1
    ).scalar() or 0
    
    # ==========================================
    # 4. Citas de hoy
    # ==========================================
    hoy = date.today()
    total_citas_hoy = db.query(func.count(Cita.id)).filter(
        func.date(Cita.fecha_hora) == hoy
    ).scalar() or 0
    
    # ==========================================
    # 5. Citas pendientes
    # ==========================================
    citas_pendientes = db.query(func.count(Cita.id)).filter(
        Cita.estado == 'PENDIENTE'
    ).scalar() or 0
    
    # ==========================================
    # 6. Progreso promedio de sesiones
    # ==========================================
    progreso_promedio_raw = db.query(
        func.avg(cast(Sesion.progreso, Float))
    ).filter(
        Sesion.progreso.isnot(None)
    ).scalar()
    
    progreso_promedio = round(float(progreso_promedio_raw), 2) if progreso_promedio_raw else 0.0
    
    # ==========================================
    # 7. Terapias más demandadas (top 5)
    # ==========================================
    terapias_mas_demandadas_query = (
        db.query(
            Terapia.nombre,
            func.count(TerapiaNino.id).label('total_asignaciones')
        )
        .join(TerapiaNino, TerapiaNino.terapia_id == Terapia.id)
        .group_by(Terapia.id, Terapia.nombre)
        .order_by(func.count(TerapiaNino.id).desc())
        .limit(5)
        .all()
    )
    
    terapias_mas_demandadas = [
        {"nombre": t[0], "total_asignaciones": t[1]}
        for t in terapias_mas_demandadas_query
    ]
    
    # ==========================================
    # 8. Terapeutas con más pacientes (top 5)
    # ==========================================
    terapeutas_con_mas_pacientes_query = (
        db.query(
            Personal.nombres,
            Personal.apellido_paterno,
            func.count(func.distinct(TerapiaNino.nino_id)).label('total_pacientes')
        )
        .join(TerapiaNino, TerapiaNino.terapeuta_id == Personal.id)
        .group_by(Personal.id, Personal.nombres, Personal.apellido_paterno)
        .order_by(func.count(func.distinct(TerapiaNino.nino_id)).desc())
        .limit(5)
        .all()
    )
    
    terapeutas_con_mas_pacientes = [
        {
            "nombre_completo": f"{t[0]} {t[1]}",
            "total_pacientes": t[2]
        }
        for t in terapeutas_con_mas_pacientes_query
    ]
    
    # ==========================================
    # 9. Niños nuevos este mes
    # ==========================================
    primer_dia_mes = datetime(hoy.year, hoy.month, 1)
    ninos_nuevos_mes = db.query(func.count(Nino.id)).filter(
        Nino.fecha_registro >= primer_dia_mes
    ).scalar() or 0
    
    # ==========================================
    # 10. Estadísticas adicionales útiles
    # ==========================================
    # Total de sesiones realizadas
    total_sesiones = db.query(func.count(Sesion.id)).scalar() or 0
    
    # Tasa de asistencia (sesiones donde asistio = 1)
    sesiones_asistidas = db.query(func.count(Sesion.id)).filter(
        Sesion.asistio == 1
    ).scalar() or 0
    
    tasa_asistencia = round(
        (sesiones_asistidas / total_sesiones * 100) if total_sesiones > 0 else 0.0,
        2
    )
    
    # ==========================================
    # Respuesta final
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
        "fecha_consulta": hoy.isoformat()
    }
