// ==========================================
// Request que envía el frontend al backend
// ==========================================
export interface TopsisRequest {
  criterios: string[];                          // ["carga", "sesiones", "rating"]
  matriz: number[][];                           // [[10,4,4.5], [8,3,4.8], [12,5,4.1]]
  pesos: number[];                              // [0.4, 0.3, 0.3]
  tipo_criterio: ("beneficio" | "costo")[];     // ["costo","costo","beneficio"]
  top_k: number;                                // cuántos resultados quieres
}


// ==========================================
// Respuesta del backend
// ==========================================
export interface TopsisResultado {
  fila: number;           // índice de la alternativa evaluada
  criterios: string[];    // lista de criterios evaluados
  score: number;          // valor final TOPSIS (0-1)
}
