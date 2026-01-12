from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.api.v1.routers.notificaciones import notificar_padre, notificar_terapeuta, MetadataNotificacion

router = APIRouter(prefix="/coordinador/sesiones", tags=["Coordinador - Sesiones"])

class SesionReprogramar(BaseModel):
    sesionId: int
    nuevaFecha: str
    nuevaHora: str
    motivo: str

class SesionCancelar(BaseModel):
    sesionId: int
    motivo: str

@router.put("/reprogramar")
def reprogramar_sesion(data: SesionReprogramar):
    """Reprograma una sesión y notifica al padre y terapeuta."""
    # Lógica de reprogramación...
    
    # Datos mock
    sesion = {
        "id": data.sesionId,
        "hijoId": 1,
        "padreId": 1,
        "terapeutaId": 1,
        "tipo": "Logopedia"
    }
    
    # Notificar al padre
    notificar_padre(
        padre_id=sesion["padreId"],
        hijo_id=sesion["hijoId"],
        tipo="SESION_REPROGRAMADA",
        mensaje=f"La sesión de {sesion['tipo']} ha sido reprogramada para el {data.nuevaFecha} a las {data.nuevaHora}. Motivo: {data.motivo}",
        metadata=MetadataNotificacion(
            relacionadoId=data.sesionId,
            relacionadoTipo="sesion",
            accion="ver_sesion",
            prioridad="alta"
        )
    )
    
    # Notificar al terapeuta
    notificar_terapeuta(
        terapeuta_id=sesion["terapeutaId"],
        tipo="HORARIO_ACTUALIZADO",
        mensaje=f"Tu sesión de {sesion['tipo']} ha sido reprogramada para el {data.nuevaFecha} a las {data.nuevaHora}",
        metadata=MetadataNotificacion(
            relacionadoId=data.sesionId,
            relacionadoTipo="sesion",
            accion="ver_calendario",
            prioridad="alta"
        )
    )
    
    return {"message": "Sesión reprogramada y notificaciones enviadas"}

@router.post("/cancelar")
def cancelar_sesion(data: SesionCancelar):
    """Cancela una sesión y notifica."""
    # Lógica de cancelación...
    
    sesion = {
        "id": data.sesionId,
        "hijoId": 1,
        "padreId": 1,
        "terapeutaId": 1,
        "tipo": "Logopedia",
        "fecha": "2026-01-15"
    }
    
    # Notificar al padre
    notificar_padre(
        padre_id=sesion["padreId"],
        hijo_id=sesion["hijoId"],
        tipo="SESION_CANCELADA",
        mensaje=f"La sesión de {sesion['tipo']} del {sesion['fecha']} ha sido cancelada. Motivo: {data.motivo}",
        metadata=MetadataNotificacion(
            relacionadoId=data.sesionId,
            relacionadoTipo="sesion",
            accion="ver_sesiones",
            prioridad="alta"
        )
    )
    
    # Notificar al terapeuta
    notificar_terapeuta(
        terapeuta_id=sesion["terapeutaId"],
        tipo="SESION_CANCELADA",
        mensaje=f"Sesión de {sesion['tipo']} del {sesion['fecha']} cancelada. Motivo: {data.motivo}",
        metadata=MetadataNotificacion(
            relacionadoId=data.sesionId,
            relacionadoTipo="sesion",
            prioridad="alta"
        )
    )
    
    return {"message": "Sesión cancelada y notificaciones enviadas"}