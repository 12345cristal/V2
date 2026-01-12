// ============================================================================
// INTERFACES PARA EL MÓDULO DE PADRES
// ============================================================================

// ============================================================================
// 1️⃣ INICIO - Tarjetas resumen
// ============================================================================

export interface ProxSesion {
  id: number;
  fecha: string; // ISO 8601 format: YYYY-MM-DD
  hora: string;
  tipoTerapia: string;
  terapeuta: string;
  location?: string;
  estado: 'confirmada' | 'pendiente' | 'cancelada' | 'realizada' | 'reprogramada';
}

export interface UltimoAvance {
  id: number;
  titulo: string;
  descripcion: string;
  fechaRegistro: string; // ISO 8601 format
  porcentajeProgreso: number;
  objetivo: string;
}

export interface PagoPendiente {
  id: number;
  descripcion: string;
  monto: number;
  fechaVencimiento: string; // ISO 8601 format
  estado: 'pagado' | 'pendiente' | 'vencido' | 'parcial';
}

export interface DocumentoNuevo {
  id: number;
  nombre: string;
  tipo: 'acuerdo' | 'reporte' | 'medico' | 'medicamento' | 'otro';
  fechaSubida: string; // ISO 8601 format
  visto: boolean;
  urlPdf?: string;
}

export interface UltimaObservacion {
  id: number;
  contenido: string;
  terapeuta: string;
  fecha: string; // ISO 8601 format
  tipoTerapia: string;
}

export interface TarjetaResumen {
  proxSesion: ProxSesion | null;
  ultimoAvance: UltimoAvance | null;
  pagosPendientes: PagoPendiente[];
  documentosNuevos: DocumentoNuevo[];
  ultimaObservacion: UltimaObservacion | null;
}

export interface HijoResumen {
  id: number;
  nombre: string;
  apellidoPaterno?: string;
  apellidoMaterno?: string;
  foto?: string;
}

export interface InicioPage {
  saludo: string; // "Buenos días", "Buenas tardes", "Buenas noches"
  hora: string;
  hijoSeleccionado: HijoResumen;
  hijosDisponibles: HijoResumen[];
  tarjetas: TarjetaResumen;
  cargando: boolean;
}

// ============================================================================
// 2️⃣ MIS HIJOS - Información clínica y administrativa
// ============================================================================

export interface Medicamento {
  id: number;
  nombre: string;
  dosis: string;
  frecuencia: string;
  razon: string;
  fechaInicio: string; // ISO 8601 format
  fechaFin?: string;
  activo: boolean;
  novedadReciente?: boolean;
  fechaActualizacion?: string;
}

export interface Alergia {
  id: number;
  nombre: string;
  severidad: 'leve' | 'moderada' | 'severa';
  reaccion: string;
}

export interface Hijo {
  id: number;
  nombre: string;
  apellidoPaterno: string;
  apellidoMaterno?: string;
  foto?: string;
  fechaNacimiento: string; // ISO 8601 format
  edad: number;
  diagnostico: string;
  cuatrimestre: number;
  fechaIngreso: string; // ISO 8601 format
  alergias: Alergia[];
  medicamentos: Medicamento[];
  visto: boolean;
  novedades: number;
}

export interface MisHijosPage {
  hijos: Hijo[];
  hijoSeleccionado?: Hijo;
  cargando: boolean;
  filtro?: string;
}

// ============================================================================
// 3️⃣ SESIONES - Información de terapias
// ============================================================================

export type EstadoSesion = 'programada' | 'realizada' | 'cancelada' | 'reprogramada';

export interface Sesion {
  id: number;
  fecha: string; // ISO 8601 format
  hora: string;
  tipoTerapia: string;
  terapeuta: string;
  estado: EstadoSesion;
  duracion: number; // en minutos
  observaciones?: string;
  grabacionVoz?: string; // URL o ruta
  bitacoraUrl?: string;
}

export interface SesionesView {
  tipo: 'hoy' | 'programadas' | 'semana';
}

export interface SesionesPage {
  vistaActual: SesionesView['tipo'];
  sesiones: Sesion[];
  sesionSeleccionada?: Sesion;
  cargando: boolean;
  filtroTerapeuta?: string;
}

// ============================================================================
// 4️⃣ HISTORIAL TERAPÉUTICO - Gráficas y visualización
// ============================================================================

export interface AsistenciaData {
  mes: string;
  programadas: number;
  realizadas: number;
  canceladas: number;
  porcentajeAsistencia: number;
}

export interface ObjetivoEvolucion {
  id: number;
  descripcion: string;
  valores: number[]; // escala 0-100
  fechas: string[]; // ISO 8601 format
  estado: 'en-progreso' | 'logrado' | 'no-logrado';
}

export interface FrecuenciaTerapia {
  tipoTerapia: string;
  sesionesCompletadas: number;
  sesionesPlaneadas: number;
  porcentaje: number;
}

export interface HistorialTerapeuticoPage {
  asistencia: AsistenciaData[];
  objetivos: ObjetivoEvolucion[];
  frecuencia: FrecuenciaTerapia[];
  periodoInicio: string; // ISO 8601 format
  periodoFin: string;
  cargando: boolean;
}

// ============================================================================
// 5️⃣ TAREAS - Continuidad en casa
// ============================================================================

export type EstadoTarea = 'pendiente' | 'realizada' | 'vencida';

export interface Tarea {
  id: number;
  titulo: string;
  descripcion: string;
  objetivo: string;
  instrucciones: string;
  recursos?: string[]; // URLs o descripciones
  fechaAsignacion: string; // ISO 8601 format
  fechaVencimiento: string;
  estado: EstadoTarea;
  asignadoPor: string;
  tipoTerapia: string;
  fechaCompletada?: string;
}

export interface TareasPage {
  tareas: Tarea[];
  filtro: 'todas' | 'pendientes' | 'realizadas' | 'vencidas';
  cargando: boolean;
  ordenar: 'fecha' | 'tipo' | 'prioridad';
}

// ============================================================================
// 6️⃣ PAGOS - Transparencia de facturación
// ============================================================================

export type MetodoPago = 'tarjeta' | 'transferencia' | 'efectivo' | 'cheque';
export type EstadoPago = 'pagado' | 'pendiente' | 'vencido' | 'parcial';

export interface Pago {
  id: number;
  fecha: string; // ISO 8601 format
  monto: number;
  metodo: MetodoPago;
  referencia: string;
  estado: EstadoPago;
  comprobante?: string; // URL
  descripcion: string;
}

export interface PlanPagos {
  id: number;
  totalPlan: number;
  montoPagado: number;
  saldoPendiente: number;
  proximaFechaPago: string; // ISO 8601 format
  ultimoPago: Pago | null;
}

export interface PagosPage {
  plan: PlanPagos;
  historialPagos: Pago[];
  estadosCuenta: {
    pagado: number;
    pendiente: number;
    vencido: number;
  };
  cargando: boolean;
}

// ============================================================================
// 7️⃣ DOCUMENTOS - Documentación oficial
// ============================================================================

export type TipoDocumento = 'acuerdo' | 'reporte' | 'medico' | 'medicamento' | 'otro';

export interface Documento {
  id: number;
  nombre: string;
  tipo: TipoDocumento;
  descripcion?: string;
  urlPdf: string;
  fechaSubida: string; // ISO 8601 format
  subidoPor: string;
  visto: boolean;
  novedadReciente: boolean;
}

export interface DocumentosPage {
  documentos: Documento[];
  filtro: TipoDocumento | 'todos';
  cargando: boolean;
  ordenar: 'fecha' | 'tipo' | 'nombre';
}

// ============================================================================
// 8️⃣ RECURSOS RECOMENDADOS - Apoyo a la familia
// ============================================================================

export type TipoRecurso = 'pdf' | 'video' | 'enlace';
export type OrganizacionRecurso = 'terapeuta' | 'objetivo';

export interface Recurso {
  id: number;
  titulo: string;
  descripcion: string;
  tipo: TipoRecurso;
  url?: string;
  archivo?: string;
  terapeuta?: string;
  objetivo?: string;
  visto: boolean;
  fechaAgregado: string; // ISO 8601 format
}

export interface RecursosPage {
  recursos: Recurso[];
  organizadoPor: OrganizacionRecurso;
  filtroTerapeuta?: string;
  filtroObjetivo?: string;
  cargando: boolean;
}

// ============================================================================
// 9️⃣ MENSAJES - Comunicación segura
// ============================================================================

export type TipoContacto = 'terapeuta' | 'coordinador' | 'administrador';
export type TipoMensaje = 'texto' | 'audio' | 'archivo';

export interface Mensaje {
  id: number;
  contenido: string;
  tipo: TipoMensaje;
  remitente: string; // nombre del contacto
  tipoRemitente: TipoContacto;
  fecha: string; // ISO 8601 format
  leido: boolean;
  archivoUrl?: string;
  respuestaA?: number; // id del mensaje original
}

export interface Chat {
  id: number;
  contacto: string;
  tipoContacto: TipoContacto;
  foto?: string;
  ultimoMensaje: Mensaje;
  noLeidosCount: number;
  historial: Mensaje[];
  hijoRelacionado?: number;
}

export interface MensajesPage {
  chats: Chat[];
  chatActual?: Chat;
  cargando: boolean;
  filtroHijo?: string;
}

// ============================================================================
// 🔔 10️⃣ NOTIFICACIONES
// ============================================================================

export type TipoNotificacion = 
  | 'nueva-sesion' 
  | 'reprogramacion' 
  | 'documento-nuevo' 
  | 'comentario-terapeuta' 
  | 'pago-proximo'
  | 'mensaje-nuevo'
  | 'tarea-vencida'
  | 'medicamento-actualizado';

export interface Notificacion {
  id: number;
  tipo: TipoNotificacion;
  titulo: string;
  contenido: string;
  fecha: string; // ISO 8601 format
  leida: boolean;
  relacionadaA?: number; // id de recurso relacionado
  enlace?: string;
}

export interface NotificacionesPage {
  notificaciones: Notificacion[];
  filtro: 'todas' | 'noLeidas';
  cargando: boolean;
}

// ============================================================================
// ⚙️ 11️⃣ PERFIL Y ACCESIBILIDAD
// ============================================================================

export type TamanoTexto = 'normal' | 'grande' | 'muy-grande';
export type TemaColor = 'claro' | 'suave' | 'oscuro' | 'alto-contraste';
export type ModoLectura = 'normal' | 'lectura' | 'dislexia';

export interface PreferenciasAccesibilidad {
  tamanoTexto: TamanoTexto;
  tema: TemaColor;
  modoLectura: ModoLectura;
  contrasteAlto: boolean;
  reducirAnimaciones: boolean;
  sonidosActivados: boolean;
}

export interface UsuarioPadre {
  id: number;
  nombre: string;
  apellidos: string;
  email: string;
  telefono: string;
  foto?: string;
  hijos: number[]; // ids de hijos
  preferenciasAccesibilidad: PreferenciasAccesibilidad;
  ultimoAcceso: string; // ISO 8601 format
}

export interface PerfilPage {
  usuario: UsuarioPadre;
  preferencias: PreferenciasAccesibilidad;
  cargando: boolean;
  cambiosPendientes: boolean;
}

// ============================================================================
// TIPOS GENÉRICOS Y UTILIDADES
// ============================================================================

export interface RespuestaApi<T> {
  exito: boolean;
  datos?: T;
  error?: string;
  mensaje?: string;
}

export interface PaginacionData {
  pagina: number;
  porPagina: number;
  total: number;
  totalPaginas: number;
}

export interface ListadoPaginado<T> {
  items: T[];
  paginacion: PaginacionData;
}

export interface FiltrosFecha {
  desde: Date;
  hasta: Date;
}
