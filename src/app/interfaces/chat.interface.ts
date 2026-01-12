export interface ChatListaItem {
  conversacionId: number;
  titulo: string;
  ultimoMensaje: string | null;
  noLeidos: number;
  ultimaActualizacion: string;
}

export interface MensajeItem {
  id: number;
  conversacionId: number;
  emisorId: number;
  tipo: 'TEXTO' | 'AUDIO' | 'ARCHIVO';
  contenido: string | null;
  createdAt: string;
  eliminado: boolean;
  senderNombre: string;
  senderRol: string;
  archivos?: MensajeArchivo[];
  archivoUrl?: string | null;
  archivoNombre?: string | null;
}

export interface MensajeArchivo {
  id: number;
  archivo_url: string;
  tipo_archivo: string | null;
  nombre_original: string | null;
  tamanio_bytes: number | null;
}

export interface ConversacionParticipante {
  usuario_id: number;
  nombre: string;
  email: string;
  rol: string;
  joined_at: string;
  last_seen_at: string | null;
  activo: boolean;
}

export interface ConversacionDetalle {
  id: number;
  nino_id: number | null;
  tipo: string;
  activa: boolean;
  created_at: string;
  participantes: ConversacionParticipante[];
}

export interface CrearConversacionRequest {
  tipo: string;
  nino_id?: number | null;
  participante_ids: number[];
}
