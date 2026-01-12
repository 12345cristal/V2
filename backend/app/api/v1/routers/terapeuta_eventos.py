from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.api.v1.routers.notificaciones import notificar_terapeuta, MetadataNotificacion

router = APIRouter(prefix="/terapeuta/eventos", tags=["Terapeuta - Eventos"])

class EventoCreate(BaseModel):
    titulo: str
    descripcion: str
    fecha: str
    terapeutasIds: list[int]
    tipo: str  # "junta", "capacitacion", "evento"

@router.post("/crear")
def crear_evento(evento: EventoCreate):
    """Crea un evento y notifica a los terapeutas."""
    evento_id = 1  # Mock
    
    # Determinar tipo de notificación
    tipo_notif = "NUEVA_JUNTA" if evento.tipo == "junta" else "EVENTO_PROXIMO"
    
    # Notificar a cada terapeuta
    for terapeuta_id in evento.terapeutasIds:
        notificar_terapeuta(
            terapeuta_id=terapeuta_id,
            tipo=tipo_notif,
            mensaje=f"📅 {evento.titulo} programado para el {evento.fecha}. {evento.descripcion}",
            metadata=MetadataNotificacion(
                relacionadoId=evento_id,
                relacionadoTipo="evento",
                accion="ver_calendario",
                prioridad="media"
            )
        )
    
    return {"message": "Evento creado y notificaciones enviadas", "eventoId": evento_id}

@router.post("/asignar-paciente")
def asignar_paciente_terapeuta(terapeuta_id: int, paciente_id: int, paciente_nombre: str):
    """Asigna un nuevo paciente a un terapeuta y notifica."""
    notificar_terapeuta(
        terapeuta_id=terapeuta_id,
        tipo="NUEVO_PACIENTE",
        mensaje=f"🆕 Nuevo paciente asignado: {paciente_nombre}. Revisa su expediente para comenzar el tratamiento.",
        metadata=MetadataNotificacion(
            relacionadoId=paciente_id,
            relacionadoTipo="paciente",
            accion="ver_expediente",
            prioridad="alta"
        )
    )
    
    return {"message": "Paciente asignado y terapeuta notificado"}