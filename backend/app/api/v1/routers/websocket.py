from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from sqlalchemy.orm import Session
from typing import Dict, Set
import json
from datetime import datetime
import logging

from ..database import get_db
from ..models import Usuario, Conversacion, ConversacionParticipante, Mensaje, MensajeArchivo, MensajeVisto, Rol
from ..dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

# Almacenar conexiones activas: {conversacion_id: {usuario_id: websocket}}
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}
        self.user_conversaciones: Dict[int, Set[int]] = {}  # usuario_id -> set(conversacion_ids)

    async def connect(self, conversacion_id: int, usuario_id: int, websocket: WebSocket):
        """Registra una nueva conexión"""
        await websocket.accept()
        
        if conversacion_id not in self.active_connections:
            self.active_connections[conversacion_id] = {}
        
        self.active_connections[conversacion_id][usuario_id] = websocket
        
        if usuario_id not in self.user_conversaciones:
            self.user_conversaciones[usuario_id] = set()
        
        self.user_conversaciones[usuario_id].add(conversacion_id)
        
        logger.info(f"Usuario {usuario_id} conectado a conversación {conversacion_id}")

    def disconnect(self, conversacion_id: int, usuario_id: int):
        """Desconecta un usuario"""
        if conversacion_id in self.active_connections:
            if usuario_id in self.active_connections[conversacion_id]:
                del self.active_connections[conversacion_id][usuario_id]
                
                if not self.active_connections[conversacion_id]:
                    del self.active_connections[conversacion_id]
        
        if usuario_id in self.user_conversaciones:
            self.user_conversaciones[usuario_id].discard(conversacion_id)
        
        logger.info(f"Usuario {usuario_id} desconectado de conversación {conversacion_id}")

    async def broadcast_a_conversacion(
        self,
        conversacion_id: int,
        mensaje: dict,
        excluir_usuario: int | None = None
    ):
        """Envía un mensaje a todos en una conversación"""
        if conversacion_id not in self.active_connections:
            return
        
        desconectados = []
        
        for usuario_id, websocket in self.active_connections[conversacion_id].items():
            if excluir_usuario and usuario_id == excluir_usuario:
                continue
            
            try:
                await websocket.send_json(mensaje)
            except Exception as e:
                logger.error(f"Error enviando mensaje: {e}")
                desconectados.append(usuario_id)
        
        # Limpiar conexiones muertas
        for usuario_id in desconectados:
            self.disconnect(conversacion_id, usuario_id)

    async def broadcast_a_todos_usuarios(
        self,
        conversacion_id: int,
        mensaje: dict
    ):
        """Envía a todos incluyendo al emisor"""
        await self.broadcast_a_conversacion(conversacion_id, mensaje, excluir_usuario=None)

    def obtener_usuarios_conectados(self, conversacion_id: int) -> list:
        """Obtiene lista de usuarios conectados en una conversación"""
        if conversacion_id not in self.active_connections:
            return []
        return list(self.active_connections[conversacion_id].keys())

    async def notificar_escribiendo(self, conversacion_id: int, usuario_id: int, usuario_nombre: str):
        """Notifica que un usuario está escribiendo"""
        await self.broadcast_a_conversacion(
            conversacion_id,
            {
                "tipo": "usuario_escribiendo",
                "usuario_id": usuario_id,
                "usuario_nombre": usuario_nombre,
                "timestamp": datetime.now().isoformat()
            }
        )

    async def notificar_dejo_escribir(self, conversacion_id: int, usuario_id: int):
        """Notifica que un usuario dejó de escribir"""
        await self.broadcast_a_conversacion(
            conversacion_id,
            {
                "tipo": "usuario_dejo_escribir",
                "usuario_id": usuario_id,
                "timestamp": datetime.now().isoformat()
            }
        )


manager = ConnectionManager()


async def verificar_token_websocket(token: str, db: Session) -> Usuario | None:
    """Verifica el token de autenticación en WebSocket"""
    from ..core.security import verify_token
    try:
        payload = verify_token(token)
        usuario_id = payload.get("sub")
        if usuario_id:
            return db.query(Usuario).filter(Usuario.id == usuario_id).first()
    except:
        pass
    return None


@router.websocket("/ws/conversacion/{conversacion_id}")
async def websocket_conversacion(
    websocket: WebSocket,
    conversacion_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """
    WebSocket para conversación en tiempo real.
    Protocolo:
    - Mensaje texto: {"tipo": "mensaje", "contenido": "..."}
    - Escribiendo: {"tipo": "escribiendo", "valor": true/false}
    - Nuevo mensaje (broadcast): {"tipo": "nuevo_mensaje", "id": ..., "contenido": ..., ...}
    """
    
    # Autenticar
    usuario = await verificar_token_websocket(token, db)
    if not usuario:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="No autorizado")
        return
    
    # Verificar que es participante
    es_participante = db.query(ConversacionParticipante).filter(
        ConversacionParticipante.conversacion_id == conversacion_id,
        ConversacionParticipante.usuario_id == usuario.id
    ).first()
    
    if not es_participante:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="No eres participante")
        return
    
    # Conectar
    await manager.connect(conversacion_id, usuario.id, websocket)
    
    # Notificar conexión
    rol = db.query(Rol).filter(Rol.id == es_participante.rol_id).first()
    await manager.broadcast_a_conversacion(
        conversacion_id,
        {
            "tipo": "usuario_conectado",
            "usuario_id": usuario.id,
            "usuario_nombre": usuario.nombre,
            "usuario_rol": rol.nombre if rol else usuario.rol,
            "timestamp": datetime.now().isoformat()
        },
        excluir_usuario=usuario.id
    )
    
    escribiendo_activo = False
    
    try:
        while True:
            data = await websocket.receive_json()
            tipo = data.get("tipo")
            
            # Mensaje de texto
            if tipo == "mensaje":
                contenido = data.get("contenido", "").strip()
                if not contenido:
                    continue
                
                # Guardar en BD
                nuevo_msg = Mensaje(
                    conversacion_id=conversacion_id,
                    emisor_id=usuario.id,
                    tipo="TEXTO",
                    contenido=contenido
                )
                
                db.add(nuevo_msg)
                db.flush()
                
                # Crear registros de visto para otros usuarios
                participantes = db.query(ConversacionParticipante).filter(
                    ConversacionParticipante.conversacion_id == conversacion_id,
                    ConversacionParticipante.usuario_id != usuario.id
                ).all()
                
                for p in participantes:
                    visto_registro = MensajeVisto(
                        mensaje_id=nuevo_msg.id,
                        usuario_id=p.usuario_id,
                        visto=False
                    )
                    db.add(visto_registro)
                
                db.commit()
                
                # Notificar a todos
                await manager.broadcast_a_todos_usuarios(
                    conversacion_id,
                    {
                        "tipo": "nuevo_mensaje",
                        "id": nuevo_msg.id,
                        "conversacion_id": conversacion_id,
                        "emisor_id": usuario.id,
                        "tipo_mensaje": "TEXTO",
                        "contenido": contenido,
                        "created_at": nuevo_msg.created_at.isoformat(),
                        "senderNombre": usuario.nombre,
                        "senderRol": rol.nombre if rol else usuario.rol,
                        "archivoUrl": None,
                        "archivoNombre": None
                    }
                )
                
                # Dejar de mostrar "escribiendo"
                escribiendo_activo = False
                await manager.notificar_dejo_escribir(conversacion_id, usuario.id)
            
            # Indicador de escribiendo
            elif tipo == "escribiendo":
                valor = data.get("valor", False)
                
                if valor and not escribiendo_activo:
                    escribiendo_activo = True
                    await manager.notificar_escribiendo(
                        conversacion_id,
                        usuario.id,
                        usuario.nombre
                    )
                elif not valor and escribiendo_activo:
                    escribiendo_activo = False
                    await manager.notificar_dejo_escribir(conversacion_id, usuario.id)
            
            # Mensaje de archivo
            elif tipo == "archivo":
                archivo_url = data.get("archivoUrl")
                archivo_nombre = data.get("archivoNombre")
                tipo_archivo = data.get("tipoArchivo", "ARCHIVO")
                
                nuevo_msg = Mensaje(
                    conversacion_id=conversacion_id,
                    emisor_id=usuario.id,
                    tipo="ARCHIVO" if tipo_archivo == "ARCHIVO" else "AUDIO"
                )
                
                db.add(nuevo_msg)
                db.flush()
                
                msg_archivo = MensajeArchivo(
                    mensaje_id=nuevo_msg.id,
                    archivo_url=archivo_url,
                    nombre_original=archivo_nombre,
                    tipo_archivo=tipo_archivo
                )
                
                db.add(msg_archivo)
                
                participantes = db.query(ConversacionParticipante).filter(
                    ConversacionParticipante.conversacion_id == conversacion_id,
                    ConversacionParticipante.usuario_id != usuario.id
                ).all()
                
                for p in participantes:
                    visto_registro = MensajeVisto(
                        mensaje_id=nuevo_msg.id,
                        usuario_id=p.usuario_id,
                        visto=False
                    )
                    db.add(visto_registro)
                
                db.commit()
                
                await manager.broadcast_a_todos_usuarios(
                    conversacion_id,
                    {
                        "tipo": "nuevo_mensaje",
                        "id": nuevo_msg.id,
                        "conversacion_id": conversacion_id,
                        "emisor_id": usuario.id,
                        "tipo_mensaje": "ARCHIVO" if tipo_archivo == "ARCHIVO" else "AUDIO",
                        "contenido": None,
                        "created_at": nuevo_msg.created_at.isoformat(),
                        "senderNombre": usuario.nombre,
                        "senderRol": rol.nombre if rol else usuario.rol,
                        "archivoUrl": archivo_url,
                        "archivoNombre": archivo_nombre
                    }
                )
                
                escribiendo_activo = False
                await manager.notificar_dejo_escribir(conversacion_id, usuario.id)
    
    except WebSocketDisconnect:
        manager.disconnect(conversacion_id, usuario.id)
        await manager.broadcast_a_conversacion(
            conversacion_id,
            {
                "tipo": "usuario_desconectado",
                "usuario_id": usuario.id,
                "usuario_nombre": usuario.nombre,
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        logger.error(f"Error WebSocket: {e}")
        manager.disconnect(conversacion_id, usuario.id)