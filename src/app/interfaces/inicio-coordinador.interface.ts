export interface TarjetaIndicador {
  titulo: string;
  valor: number;
  unidad?: string;
  tendencia?: 'up' | 'down' | 'flat';
}

export interface TerapeutaResumenMini {
  id_personal: number;
  nombre_completo: string;
  especialidad: string;
  pacientes: number;
  sesiones_semana: number;
  rating: number | null;
}

export interface NiñoRiesgo {
  id_nino: number;
  nombre_completo: string;
  motivo: string; // "Muchas ausencias", "Poco avance en lenguaje", etc.
  prioridad: 'ALTA' | 'MEDIA' | 'BAJA';
}

export interface DashboardCoordinador {
  fecha: string;
  indicadores: TarjetaIndicador[];
  topTerapeutas: TerapeutaResumenMini[];
  ninosEnRiesgo: NiñoRiesgo[];
  resumenIA?: string; // Texto generado por Gemini
}

