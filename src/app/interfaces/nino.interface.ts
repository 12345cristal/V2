// ============================================================
// 🧩 INTERFACES DEL SISTEMA — AUTISMO MOCHIS
// CORREGIDAS, UNIFICADAS Y SIN WARNINGS DE ANGULAR
// ============================================================

// ----------------------- DIRECCIÓN --------------------------
export interface Direccion {
  calle: string;
  numero: string;
  colonia: string;
  municipio: string;
  codigoPostal: string;
}

// ----------------------- DIAGNÓSTICO ------------------------
export interface Diagnostico {
  diagnosticoPrincipal: string;
  fechaDiagnostico: string | null;
  diagnosticosSecundarios: string[];
  especialista: string;
  institucion: string;
}

// ----------------------- ALERGIAS ---------------------------
export interface Alergias {
  medicamentos: string;
  alimentos: string;
  ambiental: string;
}

// ----------------------- MEDICAMENTOS -----------------------
export interface MedicamentoActual {
  nombre: string;
  dosis: string;
  horario: string;
}

// ----------------------- INFORMACIÓN ESCOLAR ----------------
export interface Escolar {
  escuela: string;
  grado: string;
  maestro: string;
  horarioClases: string;
  adaptaciones: string;
}

// ----------------------- TUTOR (PADRE / MADRE / LEGAL) ------
export interface Tutor {
  nombreCompleto: string;
  fechaNacimiento?: string | null;
  telefono: string;
  telefonoSecundario?: string;
  correo: string;
  ocupacion?: string;
  direccionLaboral?: string;
  esTutorLegal?: boolean;
  relacion?: string; // para tutor legal
}

// ----------------------- CONTACTO DE EMERGENCIA -------------
export interface ContactoEmergencia {
  nombreCompleto: string;
  relacion: string;
  telefono: string;
  telefonoSecundario?: string;
  direccion?: string;
}

// ----------------------- TERAPIAS ----------------------------
export interface TerapiaInfo {
  lenguaje: boolean;
  conductual: boolean;
  ocupacional: boolean;
  sensorial: boolean;
  psicologia: boolean;
}

// ----------------------- DOCUMENTOS --------------------------
export interface ArchivosNino {
  actaNacimientoUrl?: string;
  curpUrl?: string;
  comprobanteDomicilioUrl?: string;
  fotoUrl?: string;
  diagnosticoUrl?: string;
  consentimientoUrl?: string;
  hojaIngresoUrl?: string;
}

// ----------------------- ESTADO DEL NIÑO ---------------------
export type EstadoNino = 'ACTIVO' | 'BAJA_TEMPORAL' | 'INACTIVO';

// ----------------------- INTERFAZ PRINCIPAL: NIÑO -----------
export interface Nino {
  id?: number;

  // Datos personales
  nombre: string;
  apellidoPaterno: string;
  apellidoMaterno: string;
  fechaNacimiento: string;
  edad?: number;
  sexo: 'M' | 'F' | 'O';
  curp?: string;
  fotografiaUrl?: string;

  // Estructuras principales
  direccion: Direccion;
  diagnostico: Diagnostico;
  alergias: Alergias;
  medicamentosActuales: MedicamentoActual[];

  escolar: Escolar;

  // Padres / Tutores
  padre?: Tutor | null;
  madre?: Tutor | null;
  tutorLegal?: Tutor | null;

  // Contactos emergencia
  contactosEmergencia: ContactoEmergencia[];

  // Información emocional
  infoEmocional: {
    estimulosAnsiedad: string;
    cosasQueCalman: string;
    preferenciasSensoriales: string;
    cosasNoTolera: string;
    palabrasClave: string;
    formaComunicacion: string;
    nivelComprension: 'ALTO' | 'MEDIO' | 'BAJO';
  };

  // Información del centro
  infoCentro: {
    fechaIngreso: string;
    terapias: TerapiaInfo;
    horariosTerapia: string;
    terapeutaAsignado: string;
    costoMensual: number;
    modalidadPago: string;
    estado: EstadoNino;
  };

  // Archivos subidos al sistema
  archivos?: ArchivosNino;

  // Datos adicionales
  progresoGeneral?: number;
  ultimaCita?: string | null;
  proximaCita?: string | null;
}
