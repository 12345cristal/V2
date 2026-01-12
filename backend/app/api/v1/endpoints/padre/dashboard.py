# app/api/v1/endpoints/padre/dashboard.py
"""
Router para el Dashboard del Padre
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from typing import Optional

from app.api.deps import get_db_session, require_padre
from app.models.usuario import Usuario
from app.models.tutor import Tutor
from app.models.nino import Nino
from app.models.cita import Cita
from app.schemas.padre import (
    DashboardResumen, Padre, ProximaSesion, AvanceHijo, 
    ObservacionReciente
)


router = APIRouter()


@router.get("/dashboard/{padre_id}", response_model=DashboardResumen)
async def get_dashboard(
    padre_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene el resumen completo del dashboard del padre
    
    - Próxima sesión
    - Avance de hijos
    - Pagos pendientes
    - Documentos nuevos
    - Mensajes no leídos
    - Notificaciones
    - Tareas pendientes
    - Observaciones recientes
    """
    # Verificar que el padre solo acceda a su propia información
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a este dashboard"
        )
    
    # Obtener información del padre
    padre = Padre(
        id=current_user.id,
        nombres=current_user.nombres,
        apellido_paterno=current_user.apellido_paterno,
        apellido_materno=current_user.apellido_materno,
        email=current_user.email,
        telefono=current_user.telefono,
        ocupacion=tutor.ocupacion if tutor else None,
        activo=current_user.activo,
        fecha_creacion=current_user.fecha_creacion
    )
    
    # Obtener hijos del padre
    hijos = db.query(Nino).filter(
        Nino.tutor_id == padre_id,
        Nino.estado == "ACTIVO"
    ).all()
    
    # Próxima sesión (más cercana en el futuro)
    proxima_sesion = None
    ahora = datetime.now()
    proxima_cita = db.query(Cita).filter(
        Cita.nino_id.in_([h.id for h in hijos]),
        Cita.fecha >= ahora.date(),
        Cita.estado_id.in_([1, 2])  # PROGRAMADA o CONFIRMADA
    ).order_by(Cita.fecha, Cita.hora_inicio).first()
    
    if proxima_cita and proxima_cita.nino and proxima_cita.terapia:
        hijo = next((h for h in hijos if h.id == proxima_cita.nino_id), None)
        fecha_hora = datetime.combine(
            proxima_cita.fecha, 
            proxima_cita.hora_inicio
        )
        
        # Calcular duración
        hora_fin = proxima_cita.hora_fin
        hora_inicio = proxima_cita.hora_inicio
        duracion = (datetime.combine(datetime.today(), hora_fin) - 
                   datetime.combine(datetime.today(), hora_inicio)).seconds // 60
        
        proxima_sesion = ProximaSesion(
            id=proxima_cita.id,
            hijo_nombre=f"{hijo.nombre} {hijo.apellido_paterno}" if hijo else "N/A",
            terapia=proxima_cita.terapia.nombre if proxima_cita.terapia else "N/A",
            terapeuta=f"{proxima_cita.terapeuta.nombres} {proxima_cita.terapeuta.apellido_paterno}" if proxima_cita.terapeuta else "N/A",
            fecha=fecha_hora,
            duracion_minutos=duracion,
            ubicacion="Centro de Atención"
        )
    
    # Avance de hijos
    avances_hijos = []
    for hijo in hijos:
        # Calcular progreso (simulado - ajustar según lógica real)
        sesiones_mes = db.query(func.count(Cita.id)).filter(
            Cita.nino_id == hijo.id,
            Cita.fecha >= (ahora - timedelta(days=30)).date(),
            Cita.fecha <= ahora.date()
        ).scalar() or 0
        
        sesiones_completadas = db.query(func.count(Cita.id)).filter(
            Cita.nino_id == hijo.id,
            Cita.fecha >= (ahora - timedelta(days=30)).date(),
            Cita.fecha <= ahora.date(),
            Cita.estado_id == 3  # COMPLETADA
        ).scalar() or 0
        
        avances_hijos.append(AvanceHijo(
            hijo_id=hijo.id,
            hijo_nombre=f"{hijo.nombre} {hijo.apellido_paterno}",
            progreso_general=75,  # Simulado - calcular según sesiones y objetivos reales
            sesiones_mes=sesiones_mes,
            sesiones_completadas=sesiones_completadas,
            objetivos_logrados=5,  # Simulado
            objetivos_totales=10   # Simulado
        ))
    
    # Estadísticas simuladas (ajustar según modelos reales de la BD)
    pagos_pendientes = 0  # TODO: Implementar lógica de pagos
    monto_pendiente = 0.0
    documentos_nuevos = 0  # TODO: Implementar lógica de documentos
    mensajes_no_leidos = 0  # TODO: Implementar lógica de mensajes
    notificaciones_no_leidas = 0  # TODO: Implementar lógica de notificaciones
    tareas_pendientes = 0  # TODO: Implementar lógica de tareas
    observaciones_recientes = []  # TODO: Implementar lógica de observaciones
    
    return DashboardResumen(
        padre=padre,
        proxima_sesion=proxima_sesion,
        hijos=avances_hijos,
        pagos_pendientes=pagos_pendientes,
        monto_pendiente=monto_pendiente,
        documentos_nuevos=documentos_nuevos,
        mensajes_no_leidos=mensajes_no_leidos,
        notificaciones_no_leidas=notificaciones_no_leidas,
        tareas_pendientes=tareas_pendientes,
        observaciones_recientes=observaciones_recientes
    )
