/**
 * Interfaces para el sistema de mensajería
 */

/**
 * Tipos de chat disponibles
 */
export enum ITipoChat {
  PADRE_TERAPEUTA = 'PADRE_TERAPEUTA',
  PADRE_COORDINADOR = 'PADRE_COORDINADOR',
  GRUPO = 'GRUPO',
  SOPORTE = 'SOPORTE'
}

/**
 * Chat o conversación
 */
export interface IChat {
  id: number;
  tipo: ITipoChat;
  titulo?: string;
  participantes: {
    id: number;
    nombre: string;
    rol: 'PADRE' | 'TERAPEUTA' | 'COORDINADOR' | 'ADMINISTRADOR';
    foto?: string;
    activo: boolean;
    ultimaConexion?: string;
  }[];
  ninoRelacionado?: {
    id: number;
    nombre: string;
  };
  ultimoMensaje?: IMensaje;
  mensajesNoLeidos: number;
  activo: boolean;
  silenciado: boolean;
  archivado: boolean;
  fijado: boolean;
  fechaCreacion: string;
  fechaUltimaActividad: string;
}

/**
 * Mensaje individual
 */
export interface IMensaje {
  id: number;
  chatId: number;
  remitenteId: number;
  remitenteNombre: string;
  remitenteRol: 'PADRE' | 'TERAPEUTA' | 'COORDINADOR' | 'ADMINISTRADOR' | 'SISTEMA';
  remitenteFoto?: string;
  contenido: string;
  tipoContenido: 'TEXTO' | 'IMAGEN' | 'AUDIO' | 'VIDEO' | 'DOCUMENTO' | 'ENLACE';
  adjuntos?: {
    id: number;
    nombre: string;
    url: string;
    tipo: string;
    tamano: number;
  }[];
  fechaEnvio: string;
  fechaEdicion?: string;
  editado: boolean;
  leido: boolean;
  fechaLeido?: string;
  entregado: boolean;
  fechaEntregado?: string;
  respondidoA?: {
    id: number;
    contenido: string;
    remitente: string;
  };
  reacciones?: {
    emoji: string;
    usuarioId: number;
    usuarioNombre: string;
  }[];
  importante: boolean;
  eliminado: boolean;
  eliminadoParaTodos: boolean;
}
