// ==========================================
// INTERFACES PARA CRITERIOS TOPSIS
// ==========================================

/**
 * Interfaz para criterios TOPSIS
 */
export interface CriterioTopsis {
  id?: number;
  nombre: string;
  descripcion?: string;
  peso: number;
  tipo: 'beneficio' | 'costo';
  activo: number;
}

/**
 * Interfaz para input de cálculo TOPSIS
 */
export interface TopsisInput {
  ids: number[];
  matriz: number[][];
}

/**
 * Interfaz para resultado TOPSIS con ranking
 */
export interface TopsisResultado {
  nino_id?: number;       // ID del niño (para prioridad de niños)
  fila?: number;          // índice de la alternativa evaluada (para terapeutas)
  criterios?: string[];   // lista de criterios evaluados
  score: number;          // valor final TOPSIS (0-1)
  ranking?: number;       // posición en el ranking (1=mejor)
}

// ==========================================
// INTERFACES PARA TERAPEUTAS (COMPATIBILIDAD)
// ==========================================

/**
 * Request que envía el frontend al backend para terapeutas
 */
export interface TopsisRequest {
  criterios: string[];                          // ["carga", "sesiones", "rating"]
  matriz: number[][];                           // [[10,4,4.5], [8,3,4.8], [12,5,4.1]]
  pesos: number[];                              // [0.4, 0.3, 0.3]
  tipo_criterio: ("beneficio" | "costo")[];     // ["costo","costo","beneficio"]
  top_k: number;                                // cuántos resultados quieres
}
