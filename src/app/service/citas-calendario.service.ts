// src/app/service/citas-calendario.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

// ============================================================
// INTERFACES
// ============================================================

export interface CitaCalendarioCreate {
  nino_id: number;
  terapeuta_id: number;
  terapia_id: number;
  fecha: string; // YYYY-MM-DD
  hora_inicio: string; // HH:MM:SS
  hora_fin: string; // HH:MM:SS
  estado_id?: number;
  motivo?: string;
  observaciones?: string;
  sincronizar_google_calendar?: boolean;
}

export interface CitaCalendarioResponse {
  id_cita: number;
  nino_id: number;
  terapeuta_id: number;
  terapia_id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  estado_id: number;
  motivo?: string;
  observaciones?: string;
  
  // Google Calendar
  google_event_id?: string;
  google_calendar_link?: string;
  sincronizado_calendar: boolean;
  fecha_sincronizacion?: string;
  
  // Confirmación
  confirmada: boolean;
  fecha_confirmacion?: string;
  
  // Cancelación
  fecha_cancelacion?: string;
  motivo_cancelacion?: string;
  
  // Nombres para mostrar
  nino_nombre?: string;
  terapeuta_nombre?: string;
  terapia_nombre?: string;
  estado_nombre?: string;
}

export interface CitaReprogramar {
  nueva_fecha: string;
  nueva_hora_inicio: string;
  nueva_hora_fin: string;
  motivo?: string;
  actualizar_google_calendar?: boolean;
}

export interface CitaCancelar {
  motivo_cancelacion: string;
  eliminar_de_google_calendar?: boolean;
  crear_reposicion?: boolean;
}

export interface FiltrosCalendario {
  fecha_inicio?: string;
  fecha_fin?: string;
  terapeuta_id?: number;
  nino_id?: number;
  terapia_id?: number;
  solo_confirmadas?: boolean;
}

export interface AsignacionTerapiaMultiple {
  nino_id: number;
  terapeuta_id: number;
  terapia_id: number;
  fechas: {
    fecha: string;
    hora_inicio: string;
    hora_fin: string;
  }[];
  sincronizar_google_calendar?: boolean;
}

// ============================================================
// SERVICIO
// ============================================================

@Injectable({
  providedIn: 'root'
})
export class CitasCalendarioService {
  
  private baseUrl = `${environment.apiBaseUrl}/citas`;

  constructor(private http: HttpClient) {}

  /**
   * Crear una nueva cita con sincronización a Google Calendar
   */
  crearCita(cita: CitaCalendarioCreate): Observable<CitaCalendarioResponse> {
    return this.http.post<CitaCalendarioResponse>(`${this.baseUrl}`, {
      ...cita,
      sincronizar_google_calendar: cita.sincronizar_google_calendar ?? true
    });
  }

  /**
   * Crear múltiples citas (para asignaciones recurrentes)
   */
  crearCitasMultiples(asignaciones: CitaCalendarioCreate[]): Observable<CitaCalendarioResponse[]> {
    const requests = asignaciones.map(cita => this.crearCita(cita));
    // Retorna un array de observables que se pueden ejecutar con forkJoin
    return new Observable(observer => {
      Promise.all(requests.map(req => req.toPromise()))
        .then(results => {
          observer.next(results as CitaCalendarioResponse[]);
          observer.complete();
        })
        .catch(error => observer.error(error));
    });
  }

  /**
   * Reprogramar una cita existente
   */
  reprogramarCita(citaId: number, datos: CitaReprogramar): Observable<CitaCalendarioResponse> {
    return this.http.put<CitaCalendarioResponse>(
      `${this.baseUrl}/${citaId}/reprogramar`,
      {
        ...datos,
        actualizar_google_calendar: datos.actualizar_google_calendar ?? true
      }
    );
  }

  /**
   * Cancelar una cita
   */
  cancelarCita(citaId: number, datos: CitaCancelar): Observable<CitaCalendarioResponse> {
    return this.http.put<CitaCalendarioResponse>(
      `${this.baseUrl}/${citaId}/cancelar`,
      {
        ...datos,
        eliminar_de_google_calendar: datos.eliminar_de_google_calendar ?? true
      }
    );
  }

  /**
   * Obtener calendario con filtros
   */
  obtenerCalendario(filtros: FiltrosCalendario = {}): Observable<CitaCalendarioResponse[]> {
    // El backend actual solo acepta 'fecha' exacta; este método no se usa directamente
    // Preferimos listar por día con 'listarPorFecha'
    let params = new HttpParams();
    if (filtros.terapeuta_id) params = params.set('terapeuta_id', filtros.terapeuta_id.toString());
    if (filtros.nino_id) params = params.set('nino_id', filtros.nino_id.toString());
    if (filtros.terapia_id) params = params.set('terapia_id', filtros.terapia_id.toString());
    return this.http.get<any>(`${this.baseUrl}`, { params });
  }

  /**
   * Obtener detalles de una cita específica
   */
  obtenerDetalleCita(citaId: number): Observable<CitaCalendarioResponse> {
    return this.http.get<CitaCalendarioResponse>(`${this.baseUrl}/${citaId}`);
  }

  /**
   * Abrir evento en Google Calendar
   */
  abrirEnGoogleCalendar(cita: CitaCalendarioResponse): void {
    if (cita.google_calendar_link) {
      window.open(cita.google_calendar_link, '_blank');
    }
  }

  /** Listar citas por fecha exacta (YYYY-MM-DD) */
  listarPorFecha(fecha: string, filtros?: { nino_id?: number; terapeuta_id?: number; terapia_id?: number }): Observable<{ items: CitaCalendarioResponse[] }> {
    let params = new HttpParams().set('fecha', fecha).set('page', '1').set('page_size', '500');
    if (filtros?.nino_id) params = params.set('nino_id', filtros.nino_id);
    if (filtros?.terapeuta_id) params = params.set('terapeuta_id', filtros.terapeuta_id);
    if (filtros?.terapia_id) params = params.set('terapia_id', filtros.terapia_id);
    return this.http.get<{ items: CitaCalendarioResponse[] }>(`${this.baseUrl}`, { params });
  }

  /** Actualizar cita (fecha/hora/terapeuta/observaciones...) */
  actualizarCita(citaId: number, data: Partial<CitaCalendarioCreate>): Observable<CitaCalendarioResponse> {
    return this.http.put<CitaCalendarioResponse>(`${this.baseUrl}/${citaId}`, data);
  }

  /** Cambiar estado de la cita (PATCH estado) */
  cambiarEstado(citaId: number, estadoId: number): Observable<any> {
    const params = new HttpParams().set('estado_id', estadoId);
    return this.http.patch(`${this.baseUrl}/${citaId}/estado`, null, { params });
  }

  /** Eliminar cita */
  eliminarCita(citaId: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${citaId}`);
  }

  /** Catalogo de estados de cita */
  obtenerEstadosCita(): Observable<Array<{ id: number; codigo: string; nombre: string }>> {
    return this.http.get<Array<{ id: number; codigo: string; nombre: string }>>(`${environment.apiBaseUrl}/estados-cita`);
  }

  /**
   * Generar fechas recurrentes (helper para frontend)
   * diasSemana: 1=Lunes, 2=Martes, 3=Miércoles, 4=Jueves, 5=Viernes, 6=Sábado
   */
  generarFechasRecurrentes(
    fechaInicio: Date,
    cantidadSemanas: number,
    diasSemana: number[],
    horaInicio: string,
    horaFin: string
  ): { fecha: string; hora_inicio: string; hora_fin: string }[] {
    const fechas: { fecha: string; hora_inicio: string; hora_fin: string }[] = [];
    const fechaActual = new Date(fechaInicio);
    
    // Alinear a inicio de semana (lunes = 1)
    const diaActual = fechaActual.getDay();
    const diasDesdeInicio = diaActual === 0 ? 6 : diaActual - 1; // Convertir: 0=Domingo->6, 1=Lunes->0, etc.
    
    for (let semana = 0; semana < cantidadSemanas; semana++) {
      for (const dia of diasSemana) {
        const fecha = new Date(fechaActual);
        // dia es 1=Lunes, convertir a offset desde inicio de semana
        const offsetDia = dia - 1; // 0=Lunes, 1=Martes, etc.
        fecha.setDate(fechaActual.getDate() + (semana * 7) + (offsetDia - diasDesdeInicio));
        
        if (fecha >= fechaInicio) {
          fechas.push({
            fecha: this.formatearFecha(fecha),
            hora_inicio: horaInicio,
            hora_fin: horaFin
          });
        }
      }
    }
    
    return fechas.sort((a, b) => a.fecha.localeCompare(b.fecha));
  }

  /**
   * Formatear fecha a YYYY-MM-DD
   */
  private formatearFecha(fecha: Date): string {
    const year = fecha.getFullYear();
    const month = String(fecha.getMonth() + 1).padStart(2, '0');
    const day = String(fecha.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  /**
   * Verificar disponibilidad de horario
   */
  verificarDisponibilidad(
    terapeutaId: number,
    fecha: string,
    horaInicio: string,
    horaFin: string
  ): Observable<{ disponible: boolean; conflictos: CitaCalendarioResponse[] }> {
    return new Observable(observer => {
      this.obtenerCalendario({
        terapeuta_id: terapeutaId,
        fecha_inicio: fecha,
        fecha_fin: fecha
      }).subscribe({
        next: (citas) => {
          const conflictos = citas.filter(cita => {
            return this.hayConflictoHorario(
              horaInicio,
              horaFin,
              cita.hora_inicio,
              cita.hora_fin
            );
          });
          
          observer.next({
            disponible: conflictos.length === 0,
            conflictos
          });
          observer.complete();
        },
        error: (error) => observer.error(error)
      });
    });
  }

  /**
   * Detectar conflicto de horarios
   */
  private hayConflictoHorario(
    inicio1: string,
    fin1: string,
    inicio2: string,
    fin2: string
  ): boolean {
    return (inicio1 < fin2) && (fin1 > inicio2);
  }
}




