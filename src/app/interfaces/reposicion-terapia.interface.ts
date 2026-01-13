export interface ReposicionTerapia {
  id: number;
  ninoId: number;
  ninoNombre: string;

  tipoCodigo: string;
  tipoDescripcion: string;

  fechaOriginal: string;
  horaOriginal: string;

  fechaNueva: string;
  horaNueva: string;

  motivo: string;

  estadoCodigo: string;        // "PENDING", "APPROVED"...
  estadoDescripcion: string;   // "Pendiente", "Aprobada" desde la BD

  puedeAprobar: boolean;
  puedeRechazar: boolean;
}



