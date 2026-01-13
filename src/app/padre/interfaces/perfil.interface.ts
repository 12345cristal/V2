/**
 * Interfaces para el perfil y configuración del usuario padre
 */

/**
 * Perfil completo del padre
 */
export interface IPerfilPadre {
  id: number;
  usuarioId: number;
  nombre: string;
  apellidos: string;
  nombreCompleto: string;
  email: string;
  telefono?: string;
  telefonoSecundario?: string;
  fotoPerfil?: string;
  fechaNacimiento?: string;
  edad?: number;
  genero?: 'MASCULINO' | 'FEMENINO' | 'OTRO';
  direccion?: {
    calle: string;
    numeroExterior: string;
    numeroInterior?: string;
    colonia: string;
    codigoPostal: string;
    ciudad: string;
    estado: string;
    pais: string;
  };
  ocupacion?: string;
  nivelEstudios?: string;
  hijos: {
    id: number;
    nombre: string;
    foto?: string;
  }[];
  relacionConNinos: {
    ninoId: number;
    nombreNino: string;
    parentesco: 'MAMA' | 'PAPA' | 'TUTOR' | 'OTRO';
    responsablePrincipal: boolean;
  }[];
  contactoEmergencia?: {
    nombre: string;
    telefono: string;
    relacion: string;
  };
  preferencias: IPreferenciasUsuario;
  accesibilidad: IAccesibilidad;
  fechaRegistro: string;
  ultimoAcceso?: string;
  cuentaActiva: boolean;
}

/**
 * Configuración de accesibilidad
 */
export interface IAccesibilidad {
  tamanoFuente: 'PEQUENO' | 'NORMAL' | 'GRANDE' | 'MUY_GRANDE';
  altoContraste: boolean;
  lecturaVoz: boolean;
  subtitulosAutomaticos: boolean;
  reducirAnimaciones: boolean;
  modoNoturno: boolean;
  tecladoVirtual: boolean;
  navegacionSimplificada: boolean;
  notificacionesVisuales: boolean;
  notificacionesSonoras: boolean;
  notificacionesVibracion: boolean;
}

/**
 * Preferencias del usuario
 */
export interface IPreferenciasUsuario {
  idioma: string;
  zonaHoraria: string;
  formatoFecha: 'DD/MM/YYYY' | 'MM/DD/YYYY' | 'YYYY-MM-DD';
  formatoHora: '12H' | '24H';
  monedaPreferida: string;
  notificaciones: {
    email: {
      sesiones: boolean;
      tareas: boolean;
      mensajes: boolean;
      pagos: boolean;
      documentos: boolean;
      sistema: boolean;
    };
    push: {
      sesiones: boolean;
      tareas: boolean;
      mensajes: boolean;
      pagos: boolean;
      documentos: boolean;
      sistema: boolean;
    };
    sms: {
      sesiones: boolean;
      pagos: boolean;
    };
  };
  privacidad: {
    perfilPublico: boolean;
    mostrarFoto: boolean;
    compartirProgreso: boolean;
    permitirContacto: boolean;
  };
  recordatorios: {
    anticipacionSesiones: number; // minutos
    tareasDiarias: boolean;
    horarioRecordatorioTareas?: string;
    medicamentos: boolean;
  };
  dashboard: {
    widgetsVisibles: string[];
    ordenWidgets: string[];
    vistaPreferida: 'LISTA' | 'TARJETAS' | 'CALENDARIO';
  };
}
