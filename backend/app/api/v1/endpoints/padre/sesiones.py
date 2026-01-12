# app/api/v1/endpoints/padre/sesiones.py
"""
Router para gestión de Sesiones desde el módulo Padre
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, date, timedelta, time as time_type
from typing import List, Optional

from app.api.deps import get_db_session, require_padre
from app.models.usuario import Usuario
from app.models.tutor import Tutor
from app.models.nino import Nino
from app.models.cita import Cita
from app.models.terapia import Sesion as ModelSesion
from app.schemas.padre import Sesion, SesionDetalle, SesionComentarioCreate
from app.schemas.enums import EstadoSesion


router = APIRouter()


def verificar_acceso_hijo(hijo_id: int, current_user: Usuario, db: Session) -> Nino:
    """Helper para verificar que el padre tenga acceso al hijo"""
    hijo = db.query(Nino).filter(Nino.id == hijo_id).first()
    if not hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    
    # Si es padre, verificar que sea su hijo
    if current_user.rol_id == 4:
        tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
        if not tutor or hijo.tutor_id != tutor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para acceder a esta información"
            )
    
    return hijo


@router.get("/sesiones/hoy/{hijo_id}", response_model=List[Sesion])
async def obtener_sesiones_hoy(
    hijo_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene las sesiones de hoy para el hijo
    """
    hijo = verificar_acceso_hijo(hijo_id, current_user, db)
    hoy = date.today()
    
    # Obtener citas de hoy
    citas = db.query(Cita).filter(
        Cita.nino_id == hijo_id,
        Cita.fecha == hoy
    ).order_by(Cita.hora_inicio).all()
    
    result = []
    for cita in citas:
        # Determinar estado
        estado = EstadoSesion.PROGRAMADA
        if cita.estado_id == 3:
            estado = EstadoSesion.COMPLETADA
        elif cita.estado_id == 4:
            estado = EstadoSesion.CANCELADA
        
        result.append(Sesion(
            id=cita.id,
            hijo_id=hijo_id,
            fecha=cita.fecha,
            hora_inicio=cita.hora_inicio,
            hora_fin=cita.hora_fin,
            terapia=cita.terapia.nombre if cita.terapia else "N/A",
            terapeuta=f"{cita.terapeuta.nombres} {cita.terapeuta.apellido_paterno}" if cita.terapeuta else "N/A",
            estado=estado,
            observaciones=cita.observaciones,
            asistio=True
        ))
    
    return result


@router.get("/sesiones/programadas/{hijo_id}", response_model=List[Sesion])
async def obtener_sesiones_programadas(
    hijo_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene sesiones programadas futuras para el hijo
    """
    hijo = verificar_acceso_hijo(hijo_id, current_user, db)
    hoy = date.today()
    
    # Obtener citas futuras
    citas = db.query(Cita).filter(
        Cita.nino_id == hijo_id,
        Cita.fecha > hoy,
        Cita.estado_id.in_([1, 2])  # PROGRAMADA o CONFIRMADA
    ).order_by(Cita.fecha, Cita.hora_inicio).limit(20).all()
    
    result = []
    for cita in citas:
        result.append(Sesion(
            id=cita.id,
            hijo_id=hijo_id,
            fecha=cita.fecha,
            hora_inicio=cita.hora_inicio,
            hora_fin=cita.hora_fin,
            terapia=cita.terapia.nombre if cita.terapia else "N/A",
            terapeuta=f"{cita.terapeuta.nombres} {cita.terapeuta.apellido_paterno}" if cita.terapeuta else "N/A",
            estado=EstadoSesion.PROGRAMADA,
            observaciones=cita.observaciones,
            asistio=True
        ))
    
    return result


@router.get("/sesiones/semana/{hijo_id}", response_model=List[Sesion])
async def obtener_sesiones_semana(
    hijo_id: int,
    fecha: Optional[date] = Query(None, description="Fecha de referencia (default: hoy)"),
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene sesiones de la semana para el hijo
    """
    hijo = verificar_acceso_hijo(hijo_id, current_user, db)
    
    # Usar fecha actual si no se proporciona
    fecha_ref = fecha or date.today()
    
    # Calcular inicio y fin de semana (lunes a domingo)
    dia_semana = fecha_ref.weekday()
    inicio_semana = fecha_ref - timedelta(days=dia_semana)
    fin_semana = inicio_semana + timedelta(days=6)
    
    # Obtener citas de la semana
    citas = db.query(Cita).filter(
        Cita.nino_id == hijo_id,
        Cita.fecha >= inicio_semana,
        Cita.fecha <= fin_semana
    ).order_by(Cita.fecha, Cita.hora_inicio).all()
    
    result = []
    for cita in citas:
        # Determinar estado
        estado = EstadoSesion.PROGRAMADA
        if cita.estado_id == 3:
            estado = EstadoSesion.COMPLETADA
        elif cita.estado_id == 4:
            estado = EstadoSesion.CANCELADA
        
        result.append(Sesion(
            id=cita.id,
            hijo_id=hijo_id,
            fecha=cita.fecha,
            hora_inicio=cita.hora_inicio,
            hora_fin=cita.hora_fin,
            terapia=cita.terapia.nombre if cita.terapia else "N/A",
            terapeuta=f"{cita.terapeuta.nombres} {cita.terapeuta.apellido_paterno}" if cita.terapeuta else "N/A",
            estado=estado,
            observaciones=cita.observaciones,
            asistio=True
        ))
    
    return result


@router.get("/sesiones/{sesion_id}/detalle", response_model=SesionDetalle)
async def obtener_detalle_sesion(
    sesion_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene detalles completos de una sesión
    """
    # Obtener cita
    cita = db.query(Cita).filter(Cita.id == sesion_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
    
    # Verificar acceso
    hijo = verificar_acceso_hijo(cita.nino_id, current_user, db)
    
    # Determinar estado
    estado = EstadoSesion.PROGRAMADA
    if cita.estado_id == 3:
        estado = EstadoSesion.COMPLETADA
    elif cita.estado_id == 4:
        estado = EstadoSesion.CANCELADA
    
    # Calcular duración
    hora_fin = cita.hora_fin
    hora_inicio = cita.hora_inicio
    duracion = (datetime.combine(datetime.today(), hora_fin) - 
               datetime.combine(datetime.today(), hora_inicio)).seconds // 60
    
    # TODO: Implementar lógica real para objetivos, actividades, progreso, etc.
    objetivos = []
    actividades_realizadas = []
    progreso_porcentaje = None
    comentarios_terapeuta = cita.observaciones
    materiales_usados = []
    recomendaciones = None
    
    return SesionDetalle(
        id=cita.id,
        hijo_id=cita.nino_id,
        fecha=cita.fecha,
        hora_inicio=cita.hora_inicio,
        hora_fin=cita.hora_fin,
        terapia=cita.terapia.nombre if cita.terapia else "N/A",
        terapeuta=f"{cita.terapeuta.nombres} {cita.terapeuta.apellido_paterno}" if cita.terapeuta else "N/A",
        estado=estado,
        observaciones=cita.observaciones,
        asistio=True,
        duracion_minutos=duracion,
        objetivos=objetivos,
        actividades_realizadas=actividades_realizadas,
        progreso_porcentaje=progreso_porcentaje,
        comentarios_terapeuta=comentarios_terapeuta,
        materiales_usados=materiales_usados,
        recomendaciones=recomendaciones
    )


@router.get("/sesiones/{sesion_id}/bitacora")
async def descargar_bitacora(
    sesion_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Descarga la bitácora diaria de la sesión en PDF
    """
    # Obtener cita
    cita = db.query(Cita).filter(Cita.id == sesion_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
    
    # Verificar acceso
    hijo = verificar_acceso_hijo(cita.nino_id, current_user, db)
    
    # TODO: Implementar generación de PDF de bitácora
    # Por ahora, retornar error 501
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad de descarga de bitácora en desarrollo"
    )


@router.get("/sesiones/{sesion_id}/grabacion")
async def descargar_grabacion(
    sesion_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Descarga la grabación de la sesión
    """
    # Obtener cita
    cita = db.query(Cita).filter(Cita.id == sesion_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
    
    # Verificar acceso
    hijo = verificar_acceso_hijo(cita.nino_id, current_user, db)
    
    # TODO: Implementar lógica de descarga de grabación
    # Por ahora, retornar error 501
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad de descarga de grabación en desarrollo"
    )


@router.post("/sesiones/{sesion_id}/comentarios")
async def agregar_comentarios(
    sesion_id: int,
    comentario: SesionComentarioCreate,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Terapeuta agrega comentarios a la sesión
    Solo terapeutas pueden agregar comentarios
    """
    # Verificar que sea terapeuta
    if current_user.rol_id != 3:  # Terapeuta
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo terapeutas pueden agregar comentarios a sesiones"
        )
    
    # Obtener cita
    cita = db.query(Cita).filter(Cita.id == sesion_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
    
    # Verificar que el terapeuta sea el asignado a la cita
    # (opcional, podríamos permitir que cualquier terapeuta comente)
    
    # Actualizar observaciones
    if comentario.comentario:
        cita.observaciones = comentario.comentario
    
    # TODO: Implementar campo de progreso_porcentaje en el modelo
    # TODO: Implementar campo de recomendaciones en el modelo
    
    db.commit()
    db.refresh(cita)
    
    return {
        "message": "Comentarios agregados exitosamente",
        "sesion_id": sesion_id
    }
