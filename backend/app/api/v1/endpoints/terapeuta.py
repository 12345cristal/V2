from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models import Usuario, Terapeuta, Hijo, Padre, AsignacionTerapeuta, Sesion, Progreso, Recurso, Recomendacion
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
    Obtiene todos los pacientes/hijos asignados al terapeuta actual.
    Incluye información del padre y estadísticas básicas.
    """
    if current_user.rol != "terapeuta":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo terapeutas pueden acceder a este endpoint"
        )
    
    # Obtener terapeuta
    terapeuta = db.query(Terapeuta).filter(
        Terapeuta.usuario_id == current_user.id
    ).first()
    
    if not terapeuta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Terapeuta no encontrado"
        )
    
    # Obtener asignaciones activas
    asignaciones = db.query(AsignacionTerapeuta).filter(
        AsignacionTerapeuta.terapeuta_id == terapeuta.id,
        AsignacionTerapeuta.activo == True
    ).all()
    
    hijo_ids = [asig.hijo_id for asig in asignaciones]
    
    if not hijo_ids:
        return []
    
    # Query base de hijos
    query = db.query(Hijo).filter(Hijo.id.in_(hijo_ids))
    
    # Filtro de búsqueda
    if busqueda:
        busqueda_pattern = f"%{busqueda}%"
        query = query.filter(
            (Hijo.nombre.ilike(busqueda_pattern)) |
            (Hijo.apellido.ilike(busqueda_pattern))
        )
    
    # Ordenamiento
    if orden == "nombre":
        query = query.order_by(Hijo.nombre, Hijo.apellido)
    elif orden == "edad":
        query = query.order_by(Hijo.fecha_nacimiento.desc())
    elif orden == "fecha_asignacion":
        # Necesitamos unir con asignaciones para ordenar
        pass
    
    hijos = query.all()
    
    # Construir respuesta con información completa
    resultado = []
    for hijo in hijos:
        # Obtener padre
        padre_usuario = db.query(Usuario).filter(Usuario.id == hijo.padre_id).first()
        padre = db.query(Padre).filter(Padre.usuario_id == hijo.padre_id).first()
        
        # Calcular edad
        hoy = datetime.now().date()
        edad = (hoy - hijo.fecha_nacimiento).days // 365
        
        # Obtener fecha de asignación
        asignacion = next((a for a in asignaciones if a.hijo_id == hijo.id), None)
        fecha_asignacion = asignacion.fecha_asignacion if asignacion else None
        
        # Contar sesiones
        total_sesiones = db.query(func.count(Sesion.id)).filter(
            Sesion.hijo_id == hijo.id,
            Sesion.terapeuta_id == terapeuta.id
        ).scalar()
        
        # Última sesión
        ultima_sesion = db.query(Sesion).filter(
            Sesion.hijo_id == hijo.id,
            Sesion.terapeuta_id == terapeuta.id
        ).order_by(Sesion.fecha.desc()).first()
        
        # Próxima sesión programada
        proxima_sesion = db.query(Sesion).filter(
            Sesion.hijo_id == hijo.id,
            Sesion.terapeuta_id == terapeuta.id,
            Sesion.fecha > datetime.now(),
            Sesion.estado == "programada"
        ).order_by(Sesion.fecha).first()
        
        # Recursos asignados
        recursos_asignados = db.query(func.count(Recomendacion.id)).filter(
            Recomendacion.hijo_id == hijo.id,
            Recomendacion.terapeuta_id == terapeuta.id
        ).scalar()
        
        # Nivel de progreso general
        progreso_reciente = db.query(Progreso).filter(
            Progreso.hijo_id == hijo.id
        ).order_by(Progreso.fecha.desc()).first()
        
        nivel_progreso = progreso_reciente.nivel if progreso_reciente else "No evaluado"
        
        resultado.append({
            "id": hijo.id,
            "nombre": hijo.nombre,
            "apellido": hijo.apellido,
            "edad": edad,
            "fecha_nacimiento": hijo.fecha_nacimiento.isoformat(),
            "diagnostico": hijo.diagnostico or "No especificado",
            "nivel_tea": hijo.nivel_tea or "No especificado",
            "padre_id": hijo.padre_id,
            "padre_nombre": padre_usuario.nombre if padre_usuario else "No disponible",
            "padre_email": padre_usuario.email if padre_usuario else "",
            "padre_telefono": padre.telefono if padre else "",
            "fecha_asignacion": fecha_asignacion.isoformat() if fecha_asignacion else None,
            "total_sesiones": total_sesiones or 0,
            "ultima_sesion": ultima_sesion.fecha.isoformat() if ultima_sesion else None,
            "proxima_sesion": proxima_sesion.fecha.isoformat() if proxima_sesion else None,
            "recursos_asignados": recursos_asignados or 0,
            "nivel_progreso": nivel_progreso,
            "observaciones": hijo.observaciones,
            "foto_perfil": hijo.foto_perfil
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
    if current_user.rol != "terapeuta":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo terapeutas pueden acceder"
        )
    
    terapeuta = db.query(Terapeuta).filter(
        Terapeuta.usuario_id == current_user.id
    ).first()
    
    if not terapeuta:
        raise HTTPException(status_code=404, detail="Terapeuta no encontrado")
    
    # Verificar que el hijo esté asignado al terapeuta
    asignacion = db.query(AsignacionTerapeuta).filter(
        AsignacionTerapeuta.terapeuta_id == terapeuta.id,
        AsignacionTerapeuta.hijo_id == hijo_id,
        AsignacionTerapeuta.activo == True
    ).first()
    
    if not asignacion:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este paciente"
        )
    
    # Obtener hijo
    hijo = db.query(Hijo).filter(Hijo.id == hijo_id).first()
    if not hijo:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Información del padre
    padre_usuario = db.query(Usuario).filter(Usuario.id == hijo.padre_id).first()
    padre = db.query(Padre).filter(Padre.usuario_id == hijo.padre_id).first()
    
    # Calcular edad
    hoy = datetime.now().date()
    edad = (hoy - hijo.fecha_nacimiento).days // 365
    
    # Historial de sesiones (últimas 10)
    sesiones = db.query(Sesion).filter(
        Sesion.hijo_id == hijo_id,
        Sesion.terapeuta_id == terapeuta.id
    ).order_by(Sesion.fecha.desc()).limit(10).all()
    
    sesiones_data = [{
        "id": s.id,
        "fecha": s.fecha.isoformat(),
        "tipo": s.tipo,
        "estado": s.estado,
        "duracion": s.duracion,
        "notas": s.notas,
        "objetivo": s.objetivo
    } for s in sesiones]
    
    # Progresos registrados
    progresos = db.query(Progreso).filter(
        Progreso.hijo_id == hijo_id
    ).order_by(Progreso.fecha.desc()).limit(5).all()
    
    progresos_data = [{
        "id": p.id,
        "fecha": p.fecha.isoformat(),
        "area": p.area,
        "nivel": p.nivel,
        "observaciones": p.observaciones,
        "puntuacion": p.puntuacion
    } for p in progresos]
    
    # Recursos asignados
    recomendaciones = db.query(Recomendacion).filter(
        Recomendacion.hijo_id == hijo_id,
        Recomendacion.terapeuta_id == terapeuta.id
    ).all()
    
    recursos_data = []
    for rec in recomendaciones:
        recurso = db.query(Recurso).filter(Recurso.id == rec.recurso_id).first()
        if recurso:
            recursos_data.append({
                "id": recurso.id,
                "titulo": recurso.titulo,
                "tipo": recurso.tipo_recurso,
                "categoria": recurso.categoria_recurso,
                "fecha_asignacion": rec.fecha_recomendacion.isoformat()
            })
    
    # Estadísticas generales
    total_sesiones = db.query(func.count(Sesion.id)).filter(
        Sesion.hijo_id == hijo_id,
        Sesion.terapeuta_id == terapeuta.id
    ).scalar()
    
    sesiones_completadas = db.query(func.count(Sesion.id)).filter(
        Sesion.hijo_id == hijo_id,
        Sesion.terapeuta_id == terapeuta.id,
        Sesion.estado == "completada"
    ).scalar()
    
    # Calcular tendencia de progreso (últimos 3 meses)
    tres_meses_atras = datetime.now() - timedelta(days=90)
    progresos_recientes = db.query(Progreso).filter(
        Progreso.hijo_id == hijo_id,
        Progreso.fecha >= tres_meses_atras
    ).order_by(Progreso.fecha).all()
    
    tendencia = "estable"
    if len(progresos_recientes) >= 2:
        puntuaciones = [p.puntuacion for p in progresos_recientes if p.puntuacion is not None]
        if len(puntuaciones) >= 2:
            if puntuaciones[-1] > puntuaciones[0]:
                tendencia = "mejorando"
            elif puntuaciones[-1] < puntuaciones[0]:
                tendencia = "requiere_atencion"
    
    return {
        "id": hijo.id,
        "nombre": hijo.nombre,
        "apellido": hijo.apellido,
        "edad": edad,
        "fecha_nacimiento": hijo.fecha_nacimiento.isoformat(),
        "diagnostico": hijo.diagnostico,
        "nivel_tea": hijo.nivel_tea,
        "observaciones": hijo.observaciones,
        "foto_perfil": hijo.foto_perfil,
        "padre": {
            "id": padre_usuario.id if padre_usuario else 0,
            "nombre": padre_usuario.nombre if padre_usuario else "",
            "email": padre_usuario.email if padre_usuario else "",
            "telefono": padre.telefono if padre else ""
        },
        "fecha_asignacion": asignacion.fecha_asignacion.isoformat(),
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
    if current_user.rol != "terapeuta":
        raise HTTPException(status_code=403, detail="Solo terapeutas")
    
    terapeuta = db.query(Terapeuta).filter(
        Terapeuta.usuario_id == current_user.id
    ).first()
    
    # Verificar acceso
    asignacion = db.query(AsignacionTerapeuta).filter(
        AsignacionTerapeuta.terapeuta_id == terapeuta.id,
        AsignacionTerapeuta.hijo_id == hijo_id,
        AsignacionTerapeuta.activo == True
    ).first()
    
    if not asignacion:
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
    
    # Sesiones en el período
    sesiones = db.query(Sesion).filter(
        Sesion.hijo_id == hijo_id,
        Sesion.terapeuta_id == terapeuta.id,
        Sesion.fecha >= fecha_inicio
    ).all()
    
    total_sesiones = len(sesiones)
    sesiones_completadas = len([s for s in sesiones if s.estado == "completada"])
    sesiones_canceladas = len([s for s in sesiones if s.estado == "cancelada"])
    
    # Horas totales
    horas_terapia = sum([s.duracion or 0 for s in sesiones if s.duracion]) / 60
    
    # Progresos por área
    progresos = db.query(Progreso).filter(
        Progreso.hijo_id == hijo_id,
        Progreso.fecha >= fecha_inicio
    ).all()
    
    areas_progreso = {}
    for p in progresos:
        if p.area not in areas_progreso:
            areas_progreso[p.area] = []
        if p.puntuacion is not None:
            areas_progreso[p.area].append(p.puntuacion)
    
    progresos_por_area = []
    for area, puntuaciones in areas_progreso.items():
        if puntuaciones:
            promedio = sum(puntuaciones) / len(puntuaciones)
            progresos_por_area.append({
                "area": area,
                "promedio": round(promedio, 2),
                "evaluaciones": len(puntuaciones)
            })
    
    # Recursos utilizados
    recursos_periodo = db.query(Recomendacion).filter(
        Recomendacion.hijo_id == hijo_id,
        Recomendacion.terapeuta_id == terapeuta.id,
        Recomendacion.fecha_recomendacion >= fecha_inicio
    ).count()
    
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
    if current_user.rol != "terapeuta":
        raise HTTPException(status_code=403, detail="Solo terapeutas")
    
    terapeuta = db.query(Terapeuta).filter(
        Terapeuta.usuario_id == current_user.id
    ).first()
    
    if not terapeuta:
        raise HTTPException(status_code=404, detail="Terapeuta no encontrado")
    
    # Total de pacientes activos
    total_pacientes = db.query(func.count(AsignacionTerapeuta.id)).filter(
        AsignacionTerapeuta.terapeuta_id == terapeuta.id,
        AsignacionTerapeuta.activo == True
    ).scalar()
    
    # Total de sesiones
    total_sesiones = db.query(func.count(Sesion.id)).filter(
        Sesion.terapeuta_id == terapeuta.id
    ).scalar()
    
    # Recursos creados
    total_recursos = db.query(func.count(Recurso.id)).filter(
        Recurso.terapeuta_id == terapeuta.id
    ).scalar()
    
    # Próximas sesiones (hoy y mañana)
    hoy = datetime.now()
    manana = hoy + timedelta(days=1)
    
    proximas_sesiones = db.query(Sesion).filter(
        Sesion.terapeuta_id == terapeuta.id,
        Sesion.fecha >= hoy,
        Sesion.fecha <= manana,
        Sesion.estado == "programada"
    ).order_by(Sesion.fecha).all()
    
    sesiones_proximas = [{
        "id": s.id,
        "fecha": s.fecha.isoformat(),
        "hijo_nombre": db.query(Hijo.nombre, Hijo.apellido).filter(Hijo.id == s.hijo_id).first(),
        "tipo": s.tipo
    } for s in proximas_sesiones]
    
    return {
        "id": terapeuta.id,
        "nombre": current_user.nombre,
        "email": current_user.email,
        "especialidad": terapeuta.especialidad,
        "cedula_profesional": terapeuta.cedula_profesional,
        "telefono": terapeuta.telefono,
        "anos_experiencia": terapeuta.anos_experiencia,
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
    """
    if current_user.rol != "terapeuta":
        raise HTTPException(status_code=403, detail="Solo terapeutas")
    
    terapeuta = db.query(Terapeuta).filter(
        Terapeuta.usuario_id == current_user.id
    ).first()
    
    if not terapeuta:
        raise HTTPException(status_code=404, detail="Terapeuta no encontrado")
    
    # Verificar que el hijo existe
    hijo = db.query(Hijo).filter(Hijo.id == hijo_id).first()
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    # Verificar que no exista asignación activa
    asignacion_existente = db.query(AsignacionTerapeuta).filter(
        AsignacionTerapeuta.terapeuta_id == terapeuta.id,
        AsignacionTerapeuta.hijo_id == hijo_id,
        AsignacionTerapeuta.activo == True
    ).first()
    
    if asignacion_existente:
        raise HTTPException(
            status_code=400,
            detail="Este paciente ya está asignado a tu cuenta"
        )
    
    # Crear asignación
    nueva_asignacion = AsignacionTerapeuta(
        terapeuta_id=terapeuta.id,
        hijo_id=hijo_id,
        fecha_asignacion=datetime.now(),
        activo=True
    )
    
    db.add(nueva_asignacion)
    db.commit()
    
    return {
        "message": "Paciente asignado exitosamente",
        "asignacion_id": nueva_asignacion.id
    }


@router.delete("/paciente/{hijo_id}/desasignar")
def desasignar_paciente(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Desactiva la asignación de un paciente (no elimina el historial).
    """
    if current_user.rol != "terapeuta":
        raise HTTPException(status_code=403, detail="Solo terapeutas")
    
    terapeuta = db.query(Terapeuta).filter(
        Terapeuta.usuario_id == current_user.id
    ).first()
    
    asignacion = db.query(AsignacionTerapeuta).filter(
        AsignacionTerapeuta.terapeuta_id == terapeuta.id,
        AsignacionTerapeuta.hijo_id == hijo_id,
        AsignacionTerapeuta.activo == True
    ).first()
    
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    
    asignacion.activo = False
    asignacion.fecha_fin = datetime.now()
    
    db.commit()
    
    return {"message": "Paciente desasignado correctamente"}
