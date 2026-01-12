from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ============================================
# SCHEMAS PARA MENSAJERÍA
# ============================================

class MensajeArchivoResponse(BaseModel):
    id: int
    archivo_url: str
    tipo_archivo: Optional[str]
    nombre_original: Optional[str]
    tamanio_bytes: Optional[int]

    class Config:
        from_attributes = True


class MensajeResponse(BaseModel):
    id: int
    conversacion_id: int
    emisor_id: int
    tipo: str  # TEXTO, AUDIO, ARCHIVO
    contenido: Optional[str]
    created_at: str
    eliminado: bool
    
    # Usuario emisor
    senderNombre: Optional[str] = None
    senderRol: Optional[str] = None
    
    # Archivos adjuntos
    archivos: Optional[List[MensajeArchivoResponse]] = []
    archivoUrl: Optional[str] = None
    archivoNombre: Optional[str] = None

    class Config:
        from_attributes = True


class ChatListaItemResponse(BaseModel):
    conversacionId: int
    titulo: str
    ultimoMensaje: Optional[str]
    noLeidos: int
    ultimaActualizacion: str

    class Config:
        from_attributes = True


class ConversacionParticipanteResponse(BaseModel):
    usuario_id: int
    nombre: str
    email: str
    rol: str
    joined_at: str
    last_seen_at: Optional[str]
    activo: bool

    class Config:
        from_attributes = True


class ConversacionDetalleResponse(BaseModel):
    id: int
    nino_id: Optional[int]
    tipo: str
    activa: bool
    created_at: str
    participantes: List[ConversacionParticipanteResponse]

    class Config:
        from_attributes = True


class MensajeCrearRequest(BaseModel):
    conversacion_id: int
    tipo: str
    contenido: Optional[str]
    archivo_url: Optional[str] = None
    nombre_archivo: Optional[str] = None
    tipo_archivo: Optional[str] = None


class ConversacionCrearRequest(BaseModel):
    tipo: str = "CHAT_GENERAL"
    nino_id: Optional[int] = None
    participante_ids: List[int]