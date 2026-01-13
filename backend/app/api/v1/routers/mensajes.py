from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from typing import List, Optional
from datetime import datetime
import shutil
from pathlib import Path

from app.db.session import get_db
from app.models import (
    Conversacion, ConversacionParticipante, Mensaje, MensajeArchivo,
    MensajeVisto, Usuario, Rol, Nino
)
from app.schemas import (
    MensajeResponse, ChatListaItemResponse, ConversacionDetalleResponse,
    MensajeCrearRequest, ConversacionCrearRequest
)
from app.dependencies import get_current_user

router = APIRouter(prefix="/mensajes", tags=["mensajes"])

UPLOAD_DIR = Path("uploads/mensajes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/chats", response_model=List[ChatListaItemResponse])
def listar_chats(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    nino_id: Optional[int] = None
):
    """
    Obtiene lista de conversaciones del usuario actual.
    Opcionalmente filtrado por hijo.
    Incluye el último mensaje y cantidad de no leídos.
    """
    # Obtener participaciones del usuario
    participaciones = db.query(ConversacionParticipante).filter(
        ConversacionParticipante.usuario_id == current_user.id,
        ConversacionParticipante.activo == True
    ).all()
    
    conversacion_ids = [p.conversacion_id for p in participaciones]
    
    if not conversacion_ids:
        return []
    
    # Query de conversaciones
    query = db.query(Conversacion).filter(
        Conversacion.id.in_(conversacion_ids),
        Conversacion.activa == True
    )
    
    if nino_id:
        query = query.filter(Conversacion.nino_id == nino_id)
    
    conversaciones = query.order_by(desc(Conversacion.updated_at)).all()
    
    resultado = []
    
    for conv in conversaciones:
        # Obtener último mensaje
        ultimo_msg = db.query(Mensaje).filter(
            Mensaje.conversacion_id == conv.id,
            Mensaje.eliminado == False
        ).order_by(desc(Mensaje.created_at)).first()
        
        ultimo_mensaje = ""
        if ultimo_msg:
            if ultimo_msg.tipo == "TEXTO":
                ultimo_mensaje = ultimo_msg.contenido[:50] or ""
            elif ultimo_msg.tipo == "AUDIO":
                ultimo_mensaje = "🎤 Mensaje de audio"
            elif ultimo_msg.tipo == "ARCHIVO":
                archivo = db.query(MensajeArchivo).filter(
                    MensajeArchivo.mensaje_id == ultimo_msg.id
                ).first()
                ultimo_mensaje = f"📎 {archivo.nombre_original}" if archivo else "📎 Archivo"
        
        # Contar no leídos
        no_leidos = db.query(func.count(MensajeVisto.id)).filter(
            MensajeVisto.usuario_id == current_user.id,
            MensajeVisto.visto == False,
            Mensaje.conversacion_id == conv.id
        ).join(Mensaje).scalar()
        
        # Construir título
        if conv.nino_id:
            nino = db.query(Nino).filter(Nino.id == conv.nino_id).first()
            titulo = f"Chat - {nino.nombre if nino else 'Niño'}"
        else:
            titulo = "Chat General"
        
        resultado.append({
            "conversacionId": conv.id,
            "titulo": titulo,
            "ultimoMensaje": ultimo_mensaje,
            "noLeidos": no_leidos or 0,
            "ultimaActualizacion": conv.updated_at.isoformat()
        })
    
    return resultado


@router.get("/conversacion/{conversacion_id}", response_model=ConversacionDetalleResponse)
def obtener_conversacion(
    conversacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene detalles de una conversación.
    Verifica que el usuario sea participante.
    """
    # Verificar que es participante
    es_participante = db.query(ConversacionParticipante).filter(
        ConversacionParticipante.conversacion_id == conversacion_id,
        ConversacionParticipante.usuario_id == current_user.id
    ).first()
    
    if not es_participante:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No eres participante de esta conversación"
        )
    
    conv = db.query(Conversacion).filter(
        Conversacion.id == conversacion_id
    ).first()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    
    # Obtener participantes con información
    participantes = db.query(ConversacionParticipante).filter(
        ConversacionParticipante.conversacion_id == conversacion_id
    ).all()
    
    participantes_data = []
    for p in participantes:
        usuario = db.query(Usuario).filter(Usuario.id == p.usuario_id).first()
        rol = db.query(Rol).filter(Rol.id == p.rol_id).first()
        
        participantes_data.append({
            "usuario_id": p.usuario_id,
            "nombre": usuario.nombre if usuario else "",
            "email": usuario.email if usuario else "",
            "rol": rol.nombre if rol else "",
            "joined_at": p.joined_at.isoformat(),
            "last_seen_at": p.last_seen_at.isoformat() if p.last_seen_at else None,
            "activo": p.activo
        })
    
    return {
        "id": conv.id,
        "nino_id": conv.nino_id,
        "tipo": conv.tipo,
        "activa": conv.activa,
        "created_at": conv.created_at.isoformat(),
        "participantes": participantes_data
    }


@router.get("/mensajes/{conversacion_id}", response_model=List[MensajeResponse])
def listar_mensajes(
    conversacion_id: int,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene mensajes de una conversación.
    Verifica que el usuario sea participante.
    Retorna ordenados por fecha ascendente.
    """
    # Verificar participación
    es_participante = db.query(ConversacionParticipante).filter(
        ConversacionParticipante.conversacion_id == conversacion_id,
        ConversacionParticipante.usuario_id == current_user.id
    ).first()
    
    if not es_participante:
        raise HTTPException(status_code=403, detail="No eres participante")
    
    mensajes = db.query(Mensaje).filter(
        Mensaje.conversacion_id == conversacion_id,
        Mensaje.eliminado == False
    ).order_by(Mensaje.created_at).offset(offset).limit(limit).all()
    
    resultado = []
    
    for msg in mensajes:
        emisor = db.query(Usuario).filter(Usuario.id == msg.emisor_id).first()
        rol = db.query(Rol).join(
            ConversacionParticipante,
            ConversacionParticipante.rol_id == Rol.id
        ).filter(
            ConversacionParticipante.conversacion_id == conversacion_id,
            ConversacionParticipante.usuario_id == msg.emisor_id
        ).first()
        
        archivo_url = None
        archivo_nombre = None
        
        if msg.tipo == "ARCHIVO" or msg.tipo == "AUDIO":
            archivo = db.query(MensajeArchivo).filter(
                MensajeArchivo.mensaje_id == msg.id
            ).first()
            if archivo:
                archivo_url = archivo.archivo_url
                archivo_nombre = archivo.nombre_original
        
        resultado.append({
            "id": msg.id,
            "conversacion_id": msg.conversacion_id,
            "emisor_id": msg.emisor_id,
            "tipo": msg.tipo,
            "contenido": msg.contenido,
            "created_at": msg.created_at.isoformat(),
            "eliminado": msg.eliminado,
            "senderNombre": emisor.nombre if emisor else "Desconocido",
            "senderRol": rol.nombre if rol else current_user.rol,
            "archivos": [],
            "archivoUrl": archivo_url,
            "archivoNombre": archivo_nombre
        })
    
    return resultado


@router.post("/enviar-texto")
def enviar_texto(
    conversacion_id: int,
    contenido: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Envía un mensaje de texto.
    """
    # Verificar participación
    es_participante = db.query(ConversacionParticipante).filter(
        ConversacionParticipante.conversacion_id == conversacion_id,
        ConversacionParticipante.usuario_id == current_user.id
    ).first()
    
    if not es_participante:
        raise HTTPException(status_code=403, detail="No eres participante")
    
    # Crear mensaje
    nuevo_msg = Mensaje(
        conversacion_id=conversacion_id,
        emisor_id=current_user.id,
        tipo="TEXTO",
        contenido=contenido
    )
    
    db.add(nuevo_msg)
    db.commit()
    db.refresh(nuevo_msg)
    
    # Actualizar conversación
    conv = db.query(Conversacion).filter(Conversacion.id == conversacion_id).first()
    if conv:
        conv.updated_at = datetime.now()
        db.commit()
    
    # Crear registros de visto para todos excepto emisor
    participantes = db.query(ConversacionParticipante).filter(
        ConversacionParticipante.conversacion_id == conversacion_id,
        ConversacionParticipante.usuario_id != current_user.id
    ).all()
    
    for p in participantes:
        visto_registro = MensajeVisto(
            mensaje_id=nuevo_msg.id,
            usuario_id=p.usuario_id,
            visto=False
        )
        db.add(visto_registro)
    
    db.commit()
    
    rol = db.query(Rol).join(
        ConversacionParticipante,
        ConversacionParticipante.rol_id == Rol.id
    ).filter(
        ConversacionParticipante.conversacion_id == conversacion_id,
        ConversacionParticipante.usuario_id == current_user.id
    ).first()
    
    return {
        "id": nuevo_msg.id,
        "conversacion_id": nuevo_msg.conversacion_id,
        "emisor_id": nuevo_msg.emisor_id,
        "tipo": "TEXTO",
        "contenido": contenido,
        "created_at": nuevo_msg.created_at.isoformat(),
        "eliminado": False,
        "senderNombre": current_user.nombre,
        "senderRol": rol.nombre if rol else current_user.rol,
        "archivos": [],
        "archivoUrl": None,
        "archivoNombre": None
    }


@router.post("/enviar-archivo")
async def enviar_archivo(
    conversacion_id: int = Form(...),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Envía un archivo o audio adjunto.
    """
    es_participante = db.query(ConversacionParticipante).filter(
        ConversacionParticipante.conversacion_id == conversacion_id,
        ConversacionParticipante.usuario_id == current_user.id
    ).first()
    
    if not es_participante:
        raise HTTPException(status_code=403, detail="No eres participante")
    
    # Guardar archivo
    filename = f"{datetime.now().timestamp()}_{archivo.filename}"
    file_path = UPLOAD_DIR / filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)
    
    archivo_url = f"/uploads/mensajes/{filename}"
    
    # Detectar tipo
    es_audio = archivo.content_type and "audio" in archivo.content_type
    tipo_msg = "AUDIO" if es_audio else "ARCHIVO"
    
    # Crear mensaje
    nuevo_msg = Mensaje(
        conversacion_id=conversacion_id,
        emisor_id=current_user.id,
        tipo=tipo_msg
    )
    
    db.add(nuevo_msg)
    db.flush()
    
    # Crear registro de archivo
    msg_archivo = MensajeArchivo(
        mensaje_id=nuevo_msg.id,
        archivo_url=archivo_url,
        tipo_archivo=archivo.content_type,
        nombre_original=archivo.filename,
        tamanio_bytes=archivo.size
    )
    
    db.add(msg_archivo)
    db.commit()
    db.refresh(nuevo_msg)
    
    # Actualizar conversación
    conv = db.query(Conversacion).filter(Conversacion.id == conversacion_id).first()
    if conv:
        conv.updated_at = datetime.now()
        db.commit()
    
    # Crear registros vistos
    participantes = db.query(ConversacionParticipante).filter(
        ConversacionParticipante.conversacion_id == conversacion_id,
        ConversacionParticipante.usuario_id != current_user.id
    ).all()
    
    for p in participantes:
        visto_registro = MensajeVisto(
            mensaje_id=nuevo_msg.id,
            usuario_id=p.usuario_id,
            visto=False
        )
        db.add(visto_registro)
    
    db.commit()
    
    rol = db.query(Rol).join(
        ConversacionParticipante,
        ConversacionParticipante.rol_id == Rol.id
    ).filter(
        ConversacionParticipante.conversacion_id == conversacion_id,
        ConversacionParticipante.usuario_id == current_user.id
    ).first()
    
    return {
        "id": nuevo_msg.id,
        "conversacion_id": nuevo_msg.conversacion_id,
        "emisor_id": nuevo_msg.emisor_id,
        "tipo": tipo_msg,
        "contenido": None,
        "created_at": nuevo_msg.created_at.isoformat(),
        "eliminado": False,
        "senderNombre": current_user.nombre,
        "senderRol": rol.nombre if rol else current_user.rol,
        "archivos": [],
        "archivoUrl": archivo_url,
        "archivoNombre": archivo.filename
    }


@router.post("/marcar-visto/{conversacion_id}")
def marcar_visto(
    conversacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Marca todos los mensajes de una conversación como visto.
    """
    es_participante = db.query(ConversacionParticipante).filter(
        ConversacionParticipante.conversacion_id == conversacion_id,
        ConversacionParticipante.usuario_id == current_user.id
    ).first()
    
    if not es_participante:
        raise HTTPException(status_code=403, detail="No eres participante")
    
    # Obtener mensajes no vistos
    vistos_pendientes = db.query(MensajeVisto).join(
        Mensaje,
        Mensaje.id == MensajeVisto.mensaje_id
    ).filter(
        Mensaje.conversacion_id == conversacion_id,
        MensajeVisto.usuario_id == current_user.id,
        MensajeVisto.visto == False
    ).all()
    
    for v in vistos_pendientes:
        v.visto = True
        v.visto_at = datetime.now()
    
    # Actualizar last_seen
    es_participante.last_seen_at = datetime.now()
    
    db.commit()
    
    return {"message": "Mensajes marcados como vistos"}


@router.post("/crear-conversacion")
def crear_conversacion(
    req: ConversacionCrearRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea una nueva conversación.
    El usuario actual es el creador y primer participante.
    """
    # Crear conversación
    nueva_conv = Conversacion(
        nino_id=req.nino_id,
        creada_por=current_user.id,
        tipo=req.tipo,
        activa=True
    )
    
    db.add(nueva_conv)
    db.flush()
    
    # Obtener rol del usuario
    rol_usuario = db.query(Rol).filter(Rol.nombre == current_user.rol).first()
    
    # Agregar creador como participante
    participante_creador = ConversacionParticipante(
        conversacion_id=nueva_conv.id,
        usuario_id=current_user.id,
        rol_id=rol_usuario.id if rol_usuario else 1,
        activo=True
    )
    db.add(participante_creador)
    
    # Agregar otros participantes
    for usuario_id in req.participante_ids:
        if usuario_id != current_user.id:
            usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
            if usuario:
                rol = db.query(Rol).filter(Rol.nombre == usuario.rol).first()
                
                participante = ConversacionParticipante(
                    conversacion_id=nueva_conv.id,
                    usuario_id=usuario_id,
                    rol_id=rol.id if rol else 1,
                    activo=True
                )
                db.add(participante)
    
    db.commit()
    db.refresh(nueva_conv)
    
    return {
        "message": "Conversación creada",
        "conversacion_id": nueva_conv.id
    }


@router.delete("/mensaje/{mensaje_id}")
def eliminar_mensaje(
    mensaje_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Elimina un mensaje (solo el emisor o admin).
    """
    msg = db.query(Mensaje).filter(Mensaje.id == mensaje_id).first()
    
    if not msg:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    if msg.emisor_id != current_user.id and current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    
    msg.eliminado = True
    db.commit()
    
    return {"message": "Mensaje eliminado"}