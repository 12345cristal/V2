# app/api/v1/endpoints/coordinador.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from typing import List
from datetime import date, datetime, timedelta

from app.api.deps import get_db_session, get_current_user
from app.models.usuario import Usuario
from app.models.personal import Personal, PersonalHorario
from app.models.nino import Nino
from app.models.cita import Cita
from app.models.terapia import TerapiaNino, Sesion, Terapia
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


@router.get("/personal/{id_personal}/datos-completos")
def obtener_datos_completos_personal(
    id_personal: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene los datos completos de un personal específico:
    - Horarios de trabajo
    - Niños asignados con sus terapias
    - Sesiones realizadas con asistencia y bitácoras
    """
    
    # Verificar que el personal existe
    personal = db.query(Personal).filter(Personal.id == id_personal).first()
    if not personal:
        return {"error": "Personal no encontrado", "horarios": [], "ninos_asignados": [], "sesiones": []}
    
    # ============================================
    # HORARIOS
    # ============================================
    horarios = (
        db.query(PersonalHorario)
        .filter(PersonalHorario.id_personal == id_personal)
        .order_by(PersonalHorario.dia_semana, PersonalHorario.hora_inicio)
        .all()
    )
    
    horarios_data = []
    for h in horarios:
        horarios_data.append({
            "id": h.id,
            "dia_semana": h.dia_semana,
            "hora_inicio": h.hora_inicio,
            "hora_fin": h.hora_fin
        })
    
    # ============================================
    # NIÑOS ASIGNADOS
    # ============================================
    terapias_asignadas = (
        db.query(TerapiaNino)
        .join(Nino, Nino.id == TerapiaNino.nino_id)
        .join(Terapia, Terapia.id == TerapiaNino.terapia_id)
        .filter(TerapiaNino.terapeuta_id == id_personal)
        .all()
    )
    
    ninos_data = []
    for ta in terapias_asignadas:
        nino = ta.nino
        terapia = ta.terapia
        ninos_data.append({
            "id_terapia_nino": ta.id,
            "id_nino": nino.id,
            "nombre_completo": f"{nino.nombre} {nino.apellido_paterno} {nino.apellido_materno or ''}".strip(),
            "foto": nino.foto,
            "terapia_nombre": terapia.nombre,
            "terapia_categoria": terapia.categoria,
            "fecha_asignacion": ta.fecha_asignacion.isoformat() if ta.fecha_asignacion else None,
            "activo": bool(ta.activo),
            "total_sesiones": len(ta.sesiones) if ta.sesiones else 0
        })
    
    # ============================================
    # SESIONES Y BITÁCORAS
    # ============================================
    sesiones = (
        db.query(Sesion)
        .join(TerapiaNino, TerapiaNino.id == Sesion.terapia_nino_id)
        .join(Nino, Nino.id == TerapiaNino.nino_id)
        .join(Terapia, Terapia.id == TerapiaNino.terapia_id)
        .filter(TerapiaNino.terapeuta_id == id_personal)
        .order_by(desc(Sesion.fecha))
        .limit(100)  # Últimas 100 sesiones
        .all()
    )
    
    sesiones_data = []
    for s in sesiones:
        nino = s.terapia_nino.nino
        terapia = s.terapia_nino.terapia
        sesiones_data.append({
            "id_sesion": s.id,
            "fecha": s.fecha,
            "id_nino": nino.id,
            "nombre_nino": f"{nino.nombre} {nino.apellido_paterno}",
            "foto_nino": nino.foto,
            "terapia_nombre": terapia.nombre,
            "asistio": bool(s.asistio),
            "progreso": s.progreso,
            "colaboracion": s.colaboracion,
            "observaciones": s.observaciones or "",
            "creado_por": s.creado_por
        })
    
    # ============================================
    # RESPUESTA
    # ============================================
    return {
        "id_personal": id_personal,
        "nombre_completo": f"{personal.nombres} {personal.apellido_paterno} {personal.apellido_materno or ''}".strip(),
        "horarios": horarios_data,
        "ninos_asignados": ninos_data,
        "sesiones": sesiones_data,
        "total_ninos": len(ninos_data),
        "total_sesiones": len(sesiones_data)
    }
