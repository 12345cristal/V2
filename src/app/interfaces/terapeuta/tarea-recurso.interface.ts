// /**
//  * Representa una tarea asignada a un niño
//  * relacionada con un recurso terapéutico
//  */
// export interface TareaRecurso {
//   /** ID único de la tarea */
//   id: number;

//   /** Recurso terapéutico asociado */
//   recurso_id: number;

//   /** Niño al que se le asigna la tarea */
//   nino_id: number;

//   /** Personal (terapeuta/coordinador) que asignó la tarea */
//   asignado_por?: number;

//   /** Fecha en que se asignó la tarea */
//   fecha_asignacion: string;

//   /** Fecha límite opcional */
//   fecha_limite?: string;

//   /** Estado de cumplimiento */
//   completado: boolean;

//   /** Comentarios escritos por padres */
//   comentarios_padres?: string;

//   /** Notas internas del terapeuta */
//   notas_terapeuta?: string;
// }
export interface TareaRecurso {
  id: number;
  recurso_id: number;
  nino_id: number;
  asignado_por?: number;
  fecha_asignacion: string;
  fecha_limite?: string;
  completado: boolean;
  comentarios_padres?: string;
  notas_terapeuta?: string;
}
