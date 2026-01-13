from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models import Usuario, Personal, Nino, Tutor, Sesion, Recurso, TerapiaNino
from app.models.recomendacion import HistorialProgreso
from app.schemas import (
    PacienteResponse, 
    PacienteDetalleResponse, 
    EstadisticasPacienteResponse,
    TerapeutaPerfilResponse
)
from ..dependencies import get_current_user

router = APIRouter(prefix="/terapeutas", tags=["terapeutas"])


@router.get("/mis-pacientes", response_model=List[PacienteResponse])
def obtener_mis_pacientes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    busqueda: Optional[str] = None,
    orden: Optional[str] = "nombre"  # nombre, edad, fecha_asignacion
):
    """
    Obtiene todos los pacientes/niños asignados al terapeuta actual.
    Incluye información del tutor y estadísticas básicas.
    """
    # Verificar que el usuario sea terapeuta (rol_id == 3)
    if current_user.rol_id != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo terapeutas pueden acceder a este endpoint"
        )
    
    # Obtener registro de Personal del terapeuta
    personal = db.query(Personal).filter(
        Personal.id_usuario == current_user.id
    ).first()
    
    if not personal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de personal no encontrado"
        )
    
    # Obtener terapias asignadas al terapeuta (TerapiaNino)
    terapias_nino = db.query(TerapiaNino).filter(
        TerapiaNino.terapeuta_id == personal.id,
        TerapiaNino.activo == 1
    ).all()
    
    nino_ids = list(set([tn.nino_id for tn in terapias_nino]))
    
    if not nino_ids:
        return []
    
    # Query base de niños
    query = db.query(Nino).filter(Nino.id.in_(nino_ids))
    
    # Filtro de búsqueda
    if busqueda:
        busqueda_pattern = f"%{busqueda}%"
        query = query.filter(
            (Nino.nombre.ilike(busqueda_pattern)) |
            (Nino.apellido_paterno.ilike(busqueda_pattern))
        )
    
    # Ordenamiento
    if orden == "nombre":
        query = query.order_by(Nino.nombre, Nino.apellido_paterno)
    elif orden == "edad":
        query = query.order_by(Nino.fecha_nacimiento.desc())
    elif orden == "fecha_asignacion":
        # Necesitamos unir con terapias para ordenar
        pass
    
    ninos = query.all()
    
    # Construir respuesta con información completa
    resultado = []
    for nino in ninos:
        # Obtener tutor
        tutor = db.query(Tutor).filter(Tutor.id == nino.tutor_id).first()
        tutor_usuario = None
        if tutor:
            tutor_usuario = db.query(Usuario).filter(Usuario.id == tutor.usuario_id).first()
        
        # Calcular edad
        hoy = datetime.now().date()
        edad = (hoy - nino.fecha_nacimiento).days // 365
        
        # Obtener fecha de asignación (primera terapia asignada)
        terapia_nino = next((tn for tn in terapias_nino if tn.nino_id == nino.id), None)
        fecha_asignacion = terapia_nino.fecha_asignacion if terapia_nino and terapia_nino.fecha_asignacion else None
        
        # Contar sesiones relacionadas con las terapias del niño
        terapia_nino_ids = [tn.id for tn in terapias_nino if tn.nino_id == nino.id]
        total_sesiones = db.query(func.count(Sesion.id)).filter(
            Sesion.terapia_nino_id.in_(terapia_nino_ids)
        ).scalar() if terapia_nino_ids else 0
        
        # Última sesión
        ultima_sesion = db.query(Sesion).filter(
            Sesion.terapia_nino_id.in_(terapia_nino_ids)
        ).order_by(Sesion.fecha.desc()).first() if terapia_nino_ids else None
        
        # Próxima sesión programada (not applicable with current Sesion model structure)
        proxima_sesion = None
        
        # Recursos asignados (skip for now as Recomendacion model structure is different)
        recursos_asignados = 0
        
        # Nivel de progreso general usando HistorialProgreso
        progreso_reciente = db.query(HistorialProgreso).filter(
            HistorialProgreso.nino_id == nino.id
        ).order_by(HistorialProgreso.fecha_sesion.desc()).first()
        
        nivel_progreso = f"{progreso_reciente.calificacion}/5" if progreso_reciente and progreso_reciente.calificacion else "No evaluado"
        
        # Obtener diagnóstico si existe
        diagnostico_info = ""
        if nino.diagnostico:
            diagnostico_info = nino.diagnostico.diagnostico_principal if nino.diagnostico.diagnostico_principal else "No especificado"
        
        resultado.append({
            "id": nino.id,
            "nombre": nino.nombre,
            "apellido": f"{nino.apellido_paterno} {nino.apellido_materno or ''}".strip(),
            "edad": edad,
            "fecha_nacimiento": nino.fecha_nacimiento.isoformat(),
            "diagnostico": diagnostico_info or "No especificado",
            "nivel_tea": "No especificado",  # Not available in Nino model
            "padre_id": tutor.id if tutor else 0,
            "padre_nombre": f"{tutor_usuario.nombres} {tutor_usuario.apellido_paterno}" if tutor_usuario else "No disponible",
            "padre_email": tutor_usuario.email if tutor_usuario else "",
            "padre_telefono": tutor_usuario.telefono if tutor_usuario else "",
            "fecha_asignacion": fecha_asignacion if fecha_asignacion else None,
            "total_sesiones": total_sesiones or 0,
            "ultima_sesion": ultima_sesion.fecha if ultima_sesion else None,
            "proxima_sesion": proxima_sesion,
            "recursos_asignados": recursos_asignados,
            "nivel_progreso": nivel_progreso,
            "observaciones": "",  # Not in current Nino model
            "foto_perfil": nino.archivos.foto_url if nino.archivos else None
        })
    
    return resultado


@router.get("/paciente/{hijo_id}", response_model=PacienteDetalleResponse)
def obtener_detalle_paciente(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene información detallada de un paciente específico.
    Incluye historial completo, objetivos, progresos y recursos.
    """
    # Verificar que el usuario sea terapeuta (rol_id == 3)
    if current_user.rol_id != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo terapeutas pueden acceder"
        )
    
    # Obtener registro de Personal del terapeuta
    personal = db.query(Personal).filter(
        Personal.id_usuario == current_user.id
    ).first()
    
    if not personal:
        raise HTTPException(status_code=404, detail="Registro de personal no encontrado")
    
    # Verificar que el niño esté asignado al terapeuta
    terapia_nino = db.query(TerapiaNino).filter(
        TerapiaNino.terapeuta_id == personal.id,
        TerapiaNino.nino_id == hijo_id,
        TerapiaNino.activo == 1
    ).first()
    
    if not terapia_nino:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este paciente"
        )
    
    # Obtener niño
    nino = db.query(Nino).filter(Nino.id == hijo_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Información del tutor
    tutor = db.query(Tutor).filter(Tutor.id == nino.tutor_id).first()
    tutor_usuario = None
    if tutor:
        tutor_usuario = db.query(Usuario).filter(Usuario.id == tutor.usuario_id).first()
    
    # Calcular edad
    hoy = datetime.now().date()
    edad = (hoy - nino.fecha_nacimiento).days // 365
    
    # Historial de sesiones (últimas 10) relacionadas con terapias del terapeuta
    terapias_nino_ids = db.query(TerapiaNino.id).filter(
        TerapiaNino.nino_id == hijo_id,
        TerapiaNino.terapeuta_id == personal.id
    ).all()
    terapias_nino_ids = [t[0] for t in terapias_nino_ids]
    
    sesiones = db.query(Sesion).filter(
        Sesion.terapia_nino_id.in_(terapias_nino_ids)
    ).order_by(Sesion.fecha.desc()).limit(10).all() if terapias_nino_ids else []
    
    sesiones_data = [{
        "id": s.id,
        "fecha": s.fecha,
        "tipo": "",  # Not available in current Sesion model
        "estado": "completada" if s.asistio else "cancelada",
        "duracion": 0,  # Not available
        "notas": s.observaciones,
        "objetivo": ""  # Not available
    } for s in sesiones]
    
    # Progresos registrados usando HistorialProgreso
    progresos = db.query(HistorialProgreso).filter(
        HistorialProgreso.nino_id == hijo_id
    ).order_by(HistorialProgreso.fecha_sesion.desc()).limit(5).all()
    
    progresos_data = [{
        "id": p.id,
        "fecha": p.fecha_sesion.isoformat(),
        "area": "",  # Not available in HistorialProgreso
        "nivel": f"{p.calificacion}/5" if p.calificacion else "N/A",
        "observaciones": p.notas_progreso,
        "puntuacion": p.calificacion
    } for p in progresos]
    
    # Recursos asignados (skip for now)
    recursos_data = []
    
    # Estadísticas generales
    total_sesiones = db.query(func.count(Sesion.id)).filter(
        Sesion.terapia_nino_id.in_(terapias_nino_ids)
    ).scalar() if terapias_nino_ids else 0
    
    sesiones_completadas = db.query(func.count(Sesion.id)).filter(
        Sesion.terapia_nino_id.in_(terapias_nino_ids),
        Sesion.asistio == 1
    ).scalar() if terapias_nino_ids else 0
    
    # Calcular tendencia de progreso (últimos 3 meses)
    tres_meses_atras = datetime.now() - timedelta(days=90)
    progresos_recientes = db.query(HistorialProgreso).filter(
        HistorialProgreso.nino_id == hijo_id,
        HistorialProgreso.fecha_sesion >= tres_meses_atras
    ).order_by(HistorialProgreso.fecha_sesion).all()
    
    tendencia = "estable"
    if len(progresos_recientes) >= 2:
        calificaciones = [p.calificacion for p in progresos_recientes if p.calificacion is not None]
        if len(calificaciones) >= 2:
            if calificaciones[-1] > calificaciones[0]:
                tendencia = "mejorando"
            elif calificaciones[-1] < calificaciones[0]:
                tendencia = "requiere_atencion"
    
    # Get diagnostico info
    diagnostico_info = ""
    if nino.diagnostico:
        diagnostico_info = nino.diagnostico.diagnostico_principal
    
    return {
        "id": nino.id,
        "nombre": nino.nombre,
        "apellido": f"{nino.apellido_paterno} {nino.apellido_materno or ''}".strip(),
        "edad": edad,
        "fecha_nacimiento": nino.fecha_nacimiento.isoformat(),
        "diagnostico": diagnostico_info,
        "nivel_tea": "",  # Not available
        "observaciones": "",  # Not available
        "foto_perfil": nino.archivos.foto_url if nino.archivos else None,
        "padre": {
            "id": tutor_usuario.id if tutor_usuario else 0,
            "nombre": f"{tutor_usuario.nombres} {tutor_usuario.apellido_paterno}" if tutor_usuario else "",
            "email": tutor_usuario.email if tutor_usuario else "",
            "telefono": tutor_usuario.telefono if tutor_usuario else ""
        },
        "fecha_asignacion": terapia_nino.fecha_asignacion if terapia_nino.fecha_asignacion else None,
        "estadisticas": {
            "total_sesiones": total_sesiones or 0,
            "sesiones_completadas": sesiones_completadas or 0,
            "recursos_asignados": len(recursos_data),
            "tendencia_progreso": tendencia
        },
        "sesiones_recientes": sesiones_data,
        "progresos": progresos_data,
        "recursos": recursos_data
    }


@router.get("/paciente/{hijo_id}/estadisticas", response_model=EstadisticasPacienteResponse)
def obtener_estadisticas_paciente(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    periodo: Optional[str] = "mes"  # semana, mes, trimestre, año
):
    """
    Obtiene estadísticas detalladas de un paciente en un período específico.
    """
    # Verificar que el usuario sea terapeuta (rol_id == 3)
    if current_user.rol_id != 3:
        raise HTTPException(status_code=403, detail="Solo terapeutas")
    
    # Obtener registro de Personal del terapeuta
    personal = db.query(Personal).filter(
        Personal.id_usuario == current_user.id
    ).first()
    
    if not personal:
        raise HTTPException(status_code=404, detail="Registro de personal no encontrado")
    
    # Verificar acceso
    terapia_nino = db.query(TerapiaNino).filter(
        TerapiaNino.terapeuta_id == personal.id,
        TerapiaNino.nino_id == hijo_id,
        TerapiaNino.activo == 1
    ).first()
    
    if not terapia_nino:
        raise HTTPException(status_code=403, detail="No tienes acceso")
    
    # Calcular fecha límite según período
    hoy = datetime.now()
    if periodo == "semana":
        fecha_inicio = hoy - timedelta(days=7)
    elif periodo == "mes":
        fecha_inicio = hoy - timedelta(days=30)
    elif periodo == "trimestre":
        fecha_inicio = hoy - timedelta(days=90)
    elif periodo == "año":
        fecha_inicio = hoy - timedelta(days=365)
    else:
        fecha_inicio = hoy - timedelta(days=30)
    
    # Obtener todas las terapias del niño con este terapeuta
    terapias_nino_ids = db.query(TerapiaNino.id).filter(
        TerapiaNino.nino_id == hijo_id,
        TerapiaNino.terapeuta_id == personal.id
    ).all()
    terapias_nino_ids = [t[0] for t in terapias_nino_ids]
    
    # Sesiones en el período
    sesiones = db.query(Sesion).filter(
        Sesion.terapia_nino_id.in_(terapias_nino_ids),
        Sesion.fecha >= fecha_inicio.strftime("%Y-%m-%d")
    ).all() if terapias_nino_ids else []
    
    total_sesiones = len(sesiones)
    sesiones_completadas = len([s for s in sesiones if s.asistio == 1])
    sesiones_canceladas = total_sesiones - sesiones_completadas
    
    # Horas totales (not available in current model, estimate)
    horas_terapia = total_sesiones * 1  # Assume 1 hour per session
    
    # Progresos por área usando HistorialProgreso
    progresos = db.query(HistorialProgreso).filter(
        HistorialProgreso.nino_id == hijo_id,
        HistorialProgreso.fecha_sesion >= fecha_inicio
    ).all()
    
    # Since HistorialProgreso doesn't have area, we'll aggregate by activity
    progresos_por_area = []
    if progresos:
        calificaciones = [p.calificacion for p in progresos if p.calificacion is not None]
        if calificaciones:
            promedio = sum(calificaciones) / len(calificaciones)
            progresos_por_area.append({
                "area": "General",
                "promedio": round(promedio, 2),
                "evaluaciones": len(calificaciones)
            })
    
    # Recursos utilizados (skip for now)
    recursos_periodo = 0
    
    return {
        "periodo": periodo,
        "fecha_inicio": fecha_inicio.isoformat(),
        "fecha_fin": hoy.isoformat(),
        "sesiones": {
            "total": total_sesiones,
            "completadas": sesiones_completadas,
            "canceladas": sesiones_canceladas,
            "tasa_asistencia": round((sesiones_completadas / total_sesiones * 100) if total_sesiones > 0 else 0, 2)
        },
        "horas_terapia": round(horas_terapia, 2),
        "progresos_por_area": progresos_por_area,
        "recursos_asignados": recursos_periodo
    }


@router.get("/perfil", response_model=TerapeutaPerfilResponse)
def obtener_perfil_terapeuta(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene el perfil completo del terapeuta actual con estadísticas generales.
    """
    # Verificar que el usuario sea terapeuta (rol_id == 3)
    if current_user.rol_id != 3:
        raise HTTPException(status_code=403, detail="Solo terapeutas")
    
    # Obtener registro de Personal del terapeuta
    personal = db.query(Personal).filter(
        Personal.id_usuario == current_user.id
    ).first()
    
    if not personal:
        raise HTTPException(status_code=404, detail="Registro de personal no encontrado")
    
    # Total de pacientes activos
    total_pacientes = db.query(func.count(TerapiaNino.id.distinct())).filter(
        TerapiaNino.terapeuta_id == personal.id,
        TerapiaNino.activo == 1
    ).scalar()
    
    # Total de sesiones
    terapias_nino_ids = db.query(TerapiaNino.id).filter(
        TerapiaNino.terapeuta_id == personal.id
    ).all()
    terapias_nino_ids = [t[0] for t in terapias_nino_ids]
    
    total_sesiones = db.query(func.count(Sesion.id)).filter(
        Sesion.terapia_nino_id.in_(terapias_nino_ids)
    ).scalar() if terapias_nino_ids else 0
    
    # Recursos creados
    total_recursos = db.query(func.count(Recurso.id)).filter(
        Recurso.personal_id == personal.id
    ).scalar()
    
    # Próximas sesiones (not applicable with current model structure)
    sesiones_proximas = []
    
    return {
        "id": personal.id,
        "nombre": f"{current_user.nombres} {current_user.apellido_paterno}",
        "email": current_user.email,
        "especialidad": personal.especialidad_principal or "",
        "cedula_profesional": personal.cedula_profesional or "",
        "telefono": current_user.telefono or "",
        "anos_experiencia": 0,  # Not directly available, would need calculation
        "estadisticas": {
            "total_pacientes": total_pacientes or 0,
            "total_sesiones": total_sesiones or 0,
            "total_recursos": total_recursos or 0,
            "sesiones_proximas": len(sesiones_proximas)
        },
        "proximas_sesiones": sesiones_proximas
    }


@router.post("/paciente/{hijo_id}/asignar")
def asignar_paciente(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Asigna un nuevo paciente al terapeuta actual.
    Nota: Este endpoint crea una relación TerapiaNino, requiere terapia_id y prioridad_id adicionales.
    """
    # Verificar que el usuario sea terapeuta (rol_id == 3)
    if current_user.rol_id != 3:
        raise HTTPException(status_code=403, detail="Solo terapeutas")
    
    # Obtener registro de Personal del terapeuta
    personal = db.query(Personal).filter(
        Personal.id_usuario == current_user.id
    ).first()
    
    if not personal:
        raise HTTPException(status_code=404, detail="Registro de personal no encontrado")
    
    # Verificar que el niño existe
    nino = db.query(Nino).filter(Nino.id == hijo_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    # Verificar que no exista asignación activa para alguna terapia
    asignacion_existente = db.query(TerapiaNino).filter(
        TerapiaNino.terapeuta_id == personal.id,
        TerapiaNino.nino_id == hijo_id,
        TerapiaNino.activo == 1
    ).first()
    
    if asignacion_existente:
        raise HTTPException(
            status_code=400,
            detail="Este paciente ya tiene terapias asignadas contigo"
        )
    
    # Nota: Este endpoint está simplificado. En un escenario real, debería:
    # 1. Recibir terapia_id y prioridad_id como parámetros
    # 2. Crear la relación TerapiaNino apropiadamente
    # Por ahora, retornamos un mensaje indicando que se necesita más información
    
    return {
        "message": "Para asignar un paciente, usa el endpoint de coordinador que permite especificar terapia y prioridad",
        "nota": "Este endpoint requiere refactorización para usar TerapiaNino correctamente"
    }


@router.delete("/paciente/{hijo_id}/desasignar")
def desasignar_paciente(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Desactiva las asignaciones de terapias de un paciente (no elimina el historial).
    """
    # Verificar que el usuario sea terapeuta (rol_id == 3)
    if current_user.rol_id != 3:
        raise HTTPException(status_code=403, detail="Solo terapeutas")
    
    # Obtener registro de Personal del terapeuta
    personal = db.query(Personal).filter(
        Personal.id_usuario == current_user.id
    ).first()
    
    if not personal:
        raise HTTPException(status_code=404, detail="Registro de personal no encontrado")
    
    # Buscar todas las terapias asignadas a este niño con este terapeuta
    terapias = db.query(TerapiaNino).filter(
        TerapiaNino.terapeuta_id == personal.id,
        TerapiaNino.nino_id == hijo_id,
        TerapiaNino.activo == 1
    ).all()
    
    if not terapias:
        raise HTTPException(status_code=404, detail="No se encontraron terapias asignadas")
    
    # Desactivar todas las terapias
    for terapia in terapias:
        terapia.activo = 0
    
    db.commit()
    
    return {"message": f"Se desactivaron {len(terapias)} terapia(s) del paciente correctamente"}
