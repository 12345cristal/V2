from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Literal
import json
from datetime import datetime

from app.db.session import get_db
from app.models.notificacion import Notificacion
from app.models.usuario import Usuario
from app.models.paciente import Paciente
from pydantic import BaseModel

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])

# ==================== MODELOS PYDANTIC ====================

class MetadataNotificacion(BaseModel):
    relacionadoId: Optional[int] = None
    relacionadoTipo: Optional[str] = None
    accion: Optional[str] = None
    prioridad: Optional[Literal["alta", "media", "baja"]] = "media"

class NotificacionResponse(BaseModel):
    id: int
    usuarioId: int
    hijoId: Optional[int]
    mensaje: str
    tipo: str
    fecha: str
    leida: bool
    metadata: Optional[dict] = None
    
    class Config:
        from_attributes = True

class NotificacionCreate(BaseModel):
    usuarioId: int
    mensaje: str
    tipo: str
    hijoId: Optional[int] = None
    metadata: Optional[MetadataNotificacion] = None

# ==================== WEBSOCKET CONNECTIONS ====================

_active_connections: Dict[str, Dict[int, List[WebSocket]]] = {
    "padre": {},
    "terapeuta": {}
}

# ==================== FUNCIONES AUXILIARES ====================

def crear_notificacion_db(
    db: Session,
    usuario_id: int,
    tipo: str,
    mensaje: str,
    hijo_id: Optional[int] = None,
    metadata: Optional[MetadataNotificacion] = None
) -> Notificacion:
    """Crea una notificación en la BD."""
    metadata_json = None
    if metadata:
        metadata_json = json.dumps(metadata.dict())
    
    notificacion = Notificacion(
        usuario_id=usuario_id,
        hijo_id=hijo_id,
        tipo=tipo,
        mensaje=mensaje,
        leida=False,
        metadata_json=metadata_json
    )
    
    db.add(notificacion)
    db.commit()
    db.refresh(notificacion)
    
    return notificacion

async def enviar_notificacion_ws(usuario_id: int, tipo_usuario: str, notificacion_dict: dict):
    """Envía notificación por WebSocket."""
    if tipo_usuario in _active_connections and usuario_id in _active_connections[tipo_usuario]:
        conexiones_muertas = []
        
        for connection in _active_connections[tipo_usuario][usuario_id]:
            try:
                await connection.send_json(notificacion_dict)
            except Exception as e:
                print(f"Error al enviar notificación: {e}")
                conexiones_muertas.append(connection)
        
        for conn in conexiones_muertas:
            _active_connections[tipo_usuario][usuario_id].remove(conn)

def notificacion_to_dict(notif: Notificacion) -> dict:
    """Convierte notificación a diccionario."""
    metadata = None
    if notif.metadata_json:
        try:
            metadata = json.loads(notif.metadata_json)
        except:
            pass
    
    return {
        "id": notif.id,
        "usuarioId": notif.usuario_id,
        "hijoId": notif.hijo_id,
        "mensaje": notif.mensaje,
        "tipo": notif.tipo,
        "fecha": notif.fecha_creacion.isoformat(),
        "leida": notif.leida,
        "metadata": metadata
    }

# ==================== FUNCIONES PÚBLICAS ====================

def notificar_padre(
    db: Session,
    padre_id: int,
    hijo_id: int,
    tipo: str,
    mensaje: str,
    metadata: Optional[MetadataNotificacion] = None
):
    """Crea notificación para padre."""
    notif = crear_notificacion_db(db, padre_id, tipo, mensaje, hijo_id, metadata)
    
    # Enviar por WebSocket (async)
    import asyncio
    try:
        asyncio.create_task(
            enviar_notificacion_ws(padre_id, "padre", notificacion_to_dict(notif))
        )
    except:
        pass
    
    return notif

def notificar_terapeuta(
    db: Session,
    terapeuta_id: int,
    tipo: str,
    mensaje: str,
    metadata: Optional[MetadataNotificacion] = None
):
    """Crea notificación para terapeuta."""
    notif = crear_notificacion_db(db, terapeuta_id, tipo, mensaje, None, metadata)
    
    # Enviar por WebSocket
    import asyncio
    try:
        asyncio.create_task(
            enviar_notificacion_ws(terapeuta_id, "terapeuta", notificacion_to_dict(notif))
        )
    except:
        pass
    
    return notif

# ==================== ENDPOINTS WEBSOCKET ====================

@router.websocket("/ws/{tipo_usuario}/{usuario_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    tipo_usuario: str,
    usuario_id: int
):
    """WebSocket para notificaciones en tiempo real."""
    if tipo_usuario not in ["padre", "terapeuta"]:
        await websocket.close(code=1003)
        return
    
    await websocket.accept()
    
    if usuario_id not in _active_connections[tipo_usuario]:
        _active_connections[tipo_usuario][usuario_id] = []
    _active_connections[tipo_usuario][usuario_id].append(websocket)
    
    print(f"✅ WebSocket conectado: {tipo_usuario} {usuario_id}")
    
    try:
        # Enviar notificaciones no leídas
        db = next(get_db())
        notificaciones = db.query(Notificacion).filter(
            Notificacion.usuario_id == usuario_id,
            Notificacion.leida == False
        ).all()
        
        for notif in notificaciones:
            await websocket.send_json(notificacion_to_dict(notif))
        
        db.close()
        
        # Mantener conexión
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    
    except WebSocketDisconnect:
        print(f"❌ WebSocket desconectado: {tipo_usuario} {usuario_id}")
    finally:
        if usuario_id in _active_connections[tipo_usuario]:
            if websocket in _active_connections[tipo_usuario][usuario_id]:
                _active_connections[tipo_usuario][usuario_id].remove(websocket)
            if not _active_connections[tipo_usuario][usuario_id]:
                del _active_connections[tipo_usuario][usuario_id]

# ==================== ENDPOINTS REST ====================

@router.get("/{tipo_usuario}/{usuario_id}", response_model=List[NotificacionResponse])
def get_notificaciones(
    tipo_usuario: str,
    usuario_id: int,
    solo_no_leidas: bool = False,
    db: Session = Depends(get_db)
):
    """Obtiene notificaciones de un usuario."""
    if tipo_usuario not in ["padre", "terapeuta"]:
        raise HTTPException(status_code=400, detail="Tipo de usuario inválido")
    
    query = db.query(Notificacion).filter(Notificacion.usuario_id == usuario_id)
    
    if solo_no_leidas:
        query = query.filter(Notificacion.leida == False)
    
    notificaciones = query.order_by(Notificacion.fecha_creacion.desc()).all()
    
    return [notificacion_to_dict(n) for n in notificaciones]

@router.put("/{notificacion_id}/marcar-leida")
def marcar_leida(notificacion_id: int, db: Session = Depends(get_db)):
    """Marca notificación como leída."""
    notif = db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()
    
    if not notif:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    
    notif.leida = True
    db.commit()
    db.refresh(notif)
    
    return notificacion_to_dict(notif)

@router.put("/{tipo_usuario}/{usuario_id}/marcar-todas-leidas")
def marcar_todas_leidas(
    tipo_usuario: str,
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """Marca todas las notificaciones como leídas."""
    if tipo_usuario not in ["padre", "terapeuta"]:
        raise HTTPException(status_code=400, detail="Tipo de usuario inválido")
    
    count = db.query(Notificacion).filter(
        Notificacion.usuario_id == usuario_id,
        Notificacion.leida == False
    ).update({"leida": True})
    
    db.commit()
    
    return {"marcadas": count}

@router.post("/crear", response_model=NotificacionResponse)
def crear_notificacion_manual(
    data: NotificacionCreate,
    db: Session = Depends(get_db)
):
    """Crea notificación manualmente."""
    notif = crear_notificacion_db(
        db,
        data.usuarioId,
        data.tipo,
        data.mensaje,
        data.hijoId,
        data.metadata
    )
    
    # Enviar por WebSocket
    tipo_usuario = "padre" if data.hijoId else "terapeuta"
    import asyncio
    try:
        asyncio.create_task(
            enviar_notificacion_ws(data.usuarioId, tipo_usuario, notificacion_to_dict(notif))
        )
    except:
        pass
    
    return notificacion_to_dict(notif)

@router.delete("/{notificacion_id}")
def eliminar_notificacion(notificacion_id: int, db: Session = Depends(get_db)):
    """Elimina notificación."""
    notif = db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()
    
    if not notif:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    
    db.delete(notif)
    db.commit()
    
    return {"message": "Notificación eliminada"}

@router.get("/stats/{tipo_usuario}/{usuario_id}")
def get_estadisticas(
    tipo_usuario: str,
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene estadísticas de notificaciones."""
    if tipo_usuario not in ["padre", "terapeuta"]:
        raise HTTPException(status_code=400, detail="Tipo de usuario inválido")
    
    notificaciones = db.query(Notificacion).filter(
        Notificacion.usuario_id == usuario_id
    ).all()
    
    total = len(notificaciones)
    no_leidas = sum(1 for n in notificaciones if not n.leida)
    leidas = total - no_leidas
    
    por_tipo = {}
    for notif in notificaciones:
        tipo = notif.tipo
        if tipo not in por_tipo:
            por_tipo[tipo] = {"total": 0, "leidas": 0, "no_leidas": 0}
        por_tipo[tipo]["total"] += 1
        if notif.leida:
            por_tipo[tipo]["leidas"] += 1
        else:
            por_tipo[tipo]["no_leidas"] += 1
    
    return {
        "total": total,
        "leidas": leidas,
        "no_leidas": no_leidas,
        "por_tipo": por_tipo
    }