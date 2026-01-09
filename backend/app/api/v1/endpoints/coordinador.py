# app/api/v1/endpoints/coordinador.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from typing import List
from datetime import date, datetime, timedelta

from app.api.deps import get_db_session, get_current_user
from app.models.usuario import Usuario
from app.models.personal import Personal
from app.models.nino import Nino
from app.models.cita import Cita
from app.schemas.coordinador import (
    DashboardCoordinador,
    TarjetaIndicador,
    TerapeutaResumenMini,
    NinoRiesgo
)

router = APIRouter()


@router.get("/dashboard", response_model=DashboardCoordinador)
def get_dashboard_coordinador(
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene datos del dashboard para el coordinador:
    - Indicadores (KPIs)
    - Top 3 terapeutas
    - Niños en riesgo
    """
    
    # ============================================
    # INDICADORES (KPIs)
    # ============================================
    
    # Total de terapeutas activos
    total_terapeutas = db.query(Personal).filter(
        Personal.estado_laboral == "ACTIVO"
    ).count()
    
    # Citas programadas esta semana
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    
    citas_semana = db.query(Cita).filter(
        and_(
            Cita.fecha >= inicio_semana,
            Cita.fecha <= fin_semana,
            Cita.estado_id == 1  # PROGRAMADA
        )
    ).count()
    
    # Total de niños activos
    total_ninos = db.query(Nino).filter(
        Nino.estado == "ACTIVO"
    ).count()
    
    indicadores = [
        TarjetaIndicador(
            titulo="Terapeutas Activos",
            valor=total_terapeutas,
            unidad="personas",
            tendencia="flat"
        ),
        TarjetaIndicador(
            titulo="Citas Esta Semana",
            valor=citas_semana,
            unidad="citas",
            tendencia="up"
        ),
        TarjetaIndicador(
            titulo="Niños Activos",
            valor=total_ninos,
            unidad="niños",
            tendencia="flat"
        )
    ]
    
    # ============================================
    # TOP 3 TERAPEUTAS (por rating)
    # ============================================
    
    top_terapeutas_query = db.query(
        Personal.id.label('id_personal'),
        func.concat(
            Personal.nombres, ' ', 
            Personal.apellido_paterno, ' ',
            func.coalesce(Personal.apellido_materno, '')
        ).label('nombre_completo'),
        Personal.especialidad_principal.label('especialidad'),
        Personal.rating,
        func.count(Cita.id).label('sesiones_semana')
    ).outerjoin(
        Cita,
        and_(
            Cita.terapeuta_id == Personal.id,
            Cita.fecha >= inicio_semana,
            Cita.fecha <= fin_semana
        )
    ).filter(
        Personal.estado_laboral == "ACTIVO"
    ).group_by(
        Personal.id
    ).order_by(
        desc(Personal.rating)
    ).limit(3).all()
    
    top_terapeutas = []
    for t in top_terapeutas_query:
        top_terapeutas.append(TerapeutaResumenMini(
            id_personal=t.id_personal,
            nombre_completo=t.nombre_completo.strip(),
            especialidad=t.especialidad or "General",
            pacientes=0,  # Puedes calcular esto si tienes la relación
            sesiones_semana=t.sesiones_semana,
            rating=float(t.rating) if t.rating else None
        ))
    
    # ============================================
    # NIÑOS EN RIESGO (lógica simple: sin citas recientes)
    # ============================================
    
    hace_15_dias = hoy - timedelta(days=15)
    
    # Niños sin citas en los últimos 15 días
    ninos_sin_citas = db.query(Nino).filter(
        Nino.estado == "ACTIVO",
        ~Nino.id.in_(
            db.query(Cita.nino_id).filter(
                Cita.fecha >= hace_15_dias
            )
        )
    ).limit(3).all()
    
    ninos_en_riesgo = []
    for nino in ninos_sin_citas:
        nombre_completo = f"{nino.nombre} {nino.apellido_paterno} {nino.apellido_materno or ''}".strip()
        ninos_en_riesgo.append(NinoRiesgo(
            id_nino=nino.id,
            nombre_completo=nombre_completo,
            motivo="Sin citas en los últimos 15 días",
            prioridad="ALTA"
        ))
    
    # ============================================
    # RESPUESTA
    # ============================================
    
    return DashboardCoordinador(
        fecha=hoy.isoformat(),
        indicadores=indicadores,
        topTerapeutas=top_terapeutas,
        ninosEnRiesgo=ninos_en_riesgo,
        resumenIA="Dashboard generado exitosamente"
    )
