# app/api/v1/endpoints/citas_calendario.py
"""
Endpoints para gestión de citas con integración de Google Calendar
Solo accesible para rol COORDINADOR
Autor: Backend Senior Developer
Fecha: 16 de diciembre de 2025
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date, time

from app.api.deps import get_db_session, require_admin_or_coordinator
from app.models.usuario import Usuario
from app.models.cita import Cita, EstadoCita
from app.models.nino import Nino
from app.models.personal import Personal
from app.models.terapia import Terapia
from app.schemas.cita import (
    CitaCreate, CitaUpdate, CitaRead, CitaCancelar, CitaReprogramar
)
from app.services.google_calendar_service import google_calendar_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


# ===================================================================
# HELPERS
# ===================================================================

def _obtener_cita_o_error(db: Session, cita_id: int) -> Cita:
    """Obtiene una cita por ID o lanza error 404"""
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cita con ID {cita_id} no encontrada"
        )
    return cita


def _construir_titulo_evento(nino: Nino, terapia: Terapia) -> str:
    """Construye el título del evento para Google Calendar"""
    return f"Terapia: {terapia.nombre} - {nino.nombres} {nino.apellido_paterno}"


def _construir_descripcion_evento(
    nino: Nino, 
    terapeuta: Optional[Personal], 
    terapia: Terapia,
    motivo: Optional[str] = None
) -> str:
    """Construye la descripción detallada del evento"""
    descripcion = f"SESIÓN DE TERAPIA\n\n"
    descripcion += f"Niño: {nino.nombres} {nino.apellido_paterno} {nino.apellido_materno or ''}\n"
    descripcion += f"Terapia: {terapia.nombre}\n"
    
    if terapeuta:
        descripcion += f"Terapeuta: {terapeuta.nombres} {terapeuta.apellido_paterno}\n"
    
    if motivo:
        descripcion += f"\nMotivo: {motivo}\n"
    
    descripcion += f"\nObjetivo: {terapia.objetivo_general or 'Sesión de terapia regular'}"
    
    return descripcion


# ===================================================================
# ENDPOINTS CRUD CON GOOGLE CALENDAR
# ===================================================================

@router.post("/", response_model=CitaRead, status_code=status.HTTP_201_CREATED)
def crear_cita(
    cita_data: CitaCreate,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    """
    **[COORDINADOR ONLY]** Crea una nueva cita y la sincroniza con Google Calendar
    
    - **nino_id**: ID del niño
    - **terapeuta_id**: ID del terapeuta asignado
    - **terapia_id**: ID del tipo de terapia
    - **fecha**: Fecha de la cita (YYYY-MM-DD)
    - **hora_inicio**: Hora de inicio (HH:MM)
    - **hora_fin**: Hora de fin (HH:MM)
    - **sincronizar_google_calendar**: Si true, crea evento en Google Calendar
    
    **Transacción:** Si falla Google Calendar, la cita se crea pero NO se sincroniza
    """
    try:
        # Validar que existan las entidades relacionadas
        nino = db.query(Nino).filter(Nino.id == cita_data.nino_id).first()
        if not nino:
            raise HTTPException(404, f"Niño con ID {cita_data.nino_id} no encontrado")
        
        terapeuta = db.query(Personal).filter(Personal.id == cita_data.terapeuta_id).first()
        if not terapeuta:
            raise HTTPException(404, f"Terapeuta con ID {cita_data.terapeuta_id} no encontrado")
        
        terapia = db.query(Terapia).filter(Terapia.id == cita_data.terapia_id).first()
        if not terapia:
            raise HTTPException(404, f"Terapia con ID {cita_data.terapia_id} no encontrada")
        
        # Crear la cita en la BD
        nueva_cita = Cita(
            **cita_data.model_dump(exclude={'sincronizar_google_calendar'}),
            creado_por=current_user.id,
            fecha_creacion=datetime.utcnow()
        )
        
        db.add(nueva_cita)
        db.flush()  # Para obtener el ID sin hacer commit
        
        # Intentar sincronizar con Google Calendar
        if cita_data.sincronizar_google_calendar and google_calendar_service.esta_configurado:
            titulo = _construir_titulo_evento(nino, terapia)
            descripcion = _construir_descripcion_evento(nino, terapeuta, terapia, cita_data.motivo)
            
            resultado_google = google_calendar_service.crear_evento(
                titulo=titulo,
                descripcion=descripcion,
                fecha=cita_data.fecha,
                hora_inicio=cita_data.hora_inicio,
                hora_fin=cita_data.hora_fin,
                ubicacion="Centro de Terapias Autismo Mochis",
                metadata={
                    'Niño ID': cita_data.nino_id,
                    'Terapeuta ID': cita_data.terapeuta_id,
                    'Terapia ID': cita_data.terapia_id,
                    'Cita ID': nueva_cita.id
                }
            )
            
            if resultado_google:
                nueva_cita.google_event_id = resultado_google['google_event_id']
                nueva_cita.google_calendar_link = resultado_google['google_calendar_link']
                nueva_cita.sincronizado_calendar = True
                nueva_cita.fecha_sincronizacion = datetime.utcnow()
                logger.info(f"✅ Cita {nueva_cita.id} sincronizada con Google Calendar")
            else:
                logger.warning(f"⚠️  Cita {nueva_cita.id} creada pero NO sincronizada con Google Calendar")
        
        db.commit()
        db.refresh(nueva_cita)
        
        # Construir respuesta
        return CitaRead(
            id_cita=nueva_cita.id,
            **cita_data.model_dump(exclude={'sincronizar_google_calendar'}),
            google_event_id=nueva_cita.google_event_id,
            google_calendar_link=nueva_cita.google_calendar_link,
            sincronizado_calendar=nueva_cita.sincronizado_calendar or False,
            fecha_sincronizacion=nueva_cita.fecha_sincronizacion,
            confirmada=nueva_cita.confirmada or False,
            fecha_confirmacion=nueva_cita.fecha_confirmacion
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al crear cita: {str(e)}")
        raise HTTPException(500, f"Error al crear cita: {str(e)}")


@router.put("/{cita_id}/reprogramar", response_model=CitaRead)
def reprogramar_cita(
    cita_id: int,
    reprogramacion: CitaReprogramar,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    """
    **[COORDINADOR ONLY]** Reprograma una cita existente
    
    - Actualiza la fecha y hora en la BD
    - Actualiza el evento en Google Calendar si está sincronizado
    - Registra el motivo de la reprogramación
    
    **Estados permitidos:** Solo se pueden reprogramar citas en estado PROGRAMADA o CONFIRMADA
    """
    try:
        cita = _obtener_cita_o_error(db, cita_id)
        
        # Validar estado
        estado = db.query(EstadoCita).filter(EstadoCita.id == cita.estado_id).first()
        if estado and estado.codigo not in ['PROGRAMADA', 'CONFIRMADA']:
            raise HTTPException(
                400, 
                f"No se puede reprogramar una cita en estado {estado.nombre}"
            )
        
        # Actualizar campos
        cita.fecha = reprogramacion.nueva_fecha
        cita.hora_inicio = reprogramacion.nueva_hora_inicio
        cita.hora_fin = reprogramacion.nueva_hora_fin
        cita.actualizado_por = current_user.id
        cita.fecha_actualizacion = datetime.utcnow()
        
        if reprogramacion.motivo:
            cita.observaciones = (cita.observaciones or "") + f"\n[REPROGRAMACIÓN {datetime.now().strftime('%Y-%m-%d %H:%M')}]: {reprogramacion.motivo}"
        
        # Actualizar en Google Calendar si está sincronizado
        if cita.google_event_id and reprogramacion.actualizar_google_calendar:
            nino = db.query(Nino).filter(Nino.id == cita.nino_id).first()
            terapia = db.query(Terapia).filter(Terapia.id == cita.terapia_id).first()
            
            if nino and terapia:
                exito = google_calendar_service.actualizar_evento(
                    google_event_id=cita.google_event_id,
                    fecha=reprogramacion.nueva_fecha,
                    hora_inicio=reprogramacion.nueva_hora_inicio,
                    hora_fin=reprogramacion.nueva_hora_fin
                )
                
                if exito:
                    cita.fecha_sincronizacion = datetime.utcnow()
                    logger.info(f"✅ Cita {cita_id} reprogramada en Google Calendar")
        
        db.commit()
        db.refresh(cita)
        
        return CitaRead(
            id_cita=cita.id,
            nino_id=cita.nino_id,
            terapeuta_id=cita.terapeuta_id,
            terapia_id=cita.terapia_id,
            fecha=cita.fecha,
            hora_inicio=cita.hora_inicio,
            hora_fin=cita.hora_fin,
            estado_id=cita.estado_id,
            motivo=cita.motivo,
            observaciones=cita.observaciones,
            es_reposicion=cita.es_reposicion,
            google_event_id=cita.google_event_id,
            google_calendar_link=cita.google_calendar_link,
            sincronizado_calendar=cita.sincronizado_calendar or False,
            fecha_sincronizacion=cita.fecha_sincronizacion,
            confirmada=cita.confirmada or False
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al reprogramar cita: {str(e)}")
        raise HTTPException(500, f"Error al reprogramar cita: {str(e)}")


@router.put("/{cita_id}/cancelar", response_model=CitaRead)
def cancelar_cita(
    cita_id: int,
    cancelacion: CitaCancelar,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    """
    **[COORDINADOR ONLY]** Cancela una cita
    
    - Cambia el estado a CANCELADA
    - Opcionalmente elimina el evento de Google Calendar
    - Registra motivo y fecha de cancelación
    - Puede crear automáticamente una sesión de reposición
    """
    try:
        cita = _obtener_cita_o_error(db, cita_id)
        
        # Obtener estado "CANCELADA"
        estado_cancelada = db.query(EstadoCita).filter(EstadoCita.codigo == 'CANCELADA').first()
        if not estado_cancelada:
            raise HTTPException(500, "Estado CANCELADA no encontrado en catálogo")
        
        # Actualizar cita
        cita.estado_id = estado_cancelada.id
        cita.motivo_cancelacion = cancelacion.motivo_cancelacion
        cita.fecha_cancelacion = datetime.utcnow()
        cita.cancelado_por = current_user.id
        cita.actualizado_por = current_user.id
        cita.fecha_actualizacion = datetime.utcnow()
        
        # Eliminar de Google Calendar si aplica
        if cita.google_event_id and cancelacion.eliminar_de_google_calendar:
            exito = google_calendar_service.eliminar_evento(cita.google_event_id)
            if exito:
                cita.sincronizado_calendar = False
                logger.info(f"✅ Cita {cita_id} eliminada de Google Calendar")
        
        # TODO: Si crear_reposicion es True, crear nueva cita de reposición
        
        db.commit()
        db.refresh(cita)
        
        return CitaRead(
            id_cita=cita.id,
            nino_id=cita.nino_id,
            terapeuta_id=cita.terapeuta_id,
            terapia_id=cita.terapia_id,
            fecha=cita.fecha,
            hora_inicio=cita.hora_inicio,
            hora_fin=cita.hora_fin,
            estado_id=cita.estado_id,
            motivo=cita.motivo,
            observaciones=cita.observaciones,
            es_reposicion=cita.es_reposicion,
            google_event_id=cita.google_event_id,
            sincronizado_calendar=cita.sincronizado_calendar or False,
            fecha_cancelacion=cita.fecha_cancelacion,
            motivo_cancelacion=cita.motivo_cancelacion
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al cancelar cita: {str(e)}")
        raise HTTPException(500, f"Error al cancelar cita: {str(e)}")


@router.get("/calendario", response_model=List[CitaRead])
def obtener_calendario(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin (YYYY-MM-DD)"),
    terapeuta_id: Optional[int] = Query(None, description="Filtrar por terapeuta"),
    nino_id: Optional[int] = Query(None, description="Filtrar por niño"),
    solo_confirmadas: bool = Query(False, description="Solo citas confirmadas"),
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    """
    **[COORDINADOR ONLY]** Obtiene las citas del calendario con filtros
    
    - Útil para construir vistas de calendario en el frontend
    - Permite filtrar por rango de fechas, terapeuta, niño
    - Incluye información de sincronización con Google Calendar
    """
    try:
        query = db.query(Cita)
        
        # Filtros
        if fecha_inicio:
            query = query.filter(Cita.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Cita.fecha <= fecha_fin)
        if terapeuta_id:
            query = query.filter(Cita.terapeuta_id == terapeuta_id)
        if nino_id:
            query = query.filter(Cita.nino_id == nino_id)
        if solo_confirmadas:
            query = query.filter(Cita.confirmada == True)
        
        citas = query.order_by(Cita.fecha, Cita.hora_inicio).all()
        
        return [
            CitaRead(
                id_cita=c.id,
                nino_id=c.nino_id,
                terapeuta_id=c.terapeuta_id,
                terapia_id=c.terapia_id,
                fecha=c.fecha,
                hora_inicio=c.hora_inicio,
                hora_fin=c.hora_fin,
                estado_id=c.estado_id,
                motivo=c.motivo,
                observaciones=c.observaciones,
                es_reposicion=c.es_reposicion,
                google_event_id=c.google_event_id,
                google_calendar_link=c.google_calendar_link,
                sincronizado_calendar=c.sincronizado_calendar or False,
                fecha_sincronizacion=c.fecha_sincronizacion,
                confirmada=c.confirmada or False,
                fecha_confirmacion=c.fecha_confirmacion
            )
            for c in citas
        ]
        
    except Exception as e:
        logger.error(f"❌ Error al obtener calendario: {str(e)}")
        raise HTTPException(500, f"Error al obtener calendario: {str(e)}")


@router.get("/{cita_id}", response_model=CitaRead)
def obtener_cita(
    cita_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    """**[COORDINADOR ONLY]** Obtiene los detalles de una cita específica"""
    cita = _obtener_cita_o_error(db, cita_id)
    
    return CitaRead(
        id_cita=cita.id,
        nino_id=cita.nino_id,
        terapeuta_id=cita.terapeuta_id,
        terapia_id=cita.terapia_id,
        fecha=cita.fecha,
        hora_inicio=cita.hora_inicio,
        hora_fin=cita.hora_fin,
        estado_id=cita.estado_id,
        motivo=cita.motivo,
        observaciones=cita.observaciones,
        es_reposicion=cita.es_reposicion,
        google_event_id=cita.google_event_id,
        google_calendar_link=cita.google_calendar_link,
        sincronizado_calendar=cita.sincronizado_calendar or False,
        fecha_sincronizacion=cita.fecha_sincronizacion,
        confirmada=cita.confirmada or False,
        fecha_confirmacion=cita.fecha_confirmacion,
        fecha_cancelacion=cita.fecha_cancelacion,
        motivo_cancelacion=cita.motivo_cancelacion
    )
