import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

export interface RegistroSesionDTO {
  id_nino: number;
  fecha: string;
  informacionClinica: {
    actividadesRealizadas: string;
    respuestaNino: string;
    observacionesClinicas?: string;
    incidentes?: string;
    evidencias?: File[];
  };
  informacionPadres: {
    resumenSesion: string;
    guiaParaCasa: {
      queHacer: string;
      queEvitar?: string;
      rutinasSugeridas?: string;
      materialesRecomendados?: string;
    };
  };
}

export interface AsistenciaDTO {
  id_sesion: number;
  estado: 'asistio' | 'cancelada' | 'reprogramada';
  fecha_registro: string;
  nota?: string;
}

export interface ReprogramacionDTO {
  id_sesion: number;
  nueva_fecha: string;
  nueva_hora: string;
  motivo: string;
}

export interface ReporteDTO {
  id_nino: number;
  cuatrimestre: string;
  archivo: File;
  tipo_reporte: 'clinico' | 'plan_intervencion';
  observaciones?: string;
}

@Injectable({
  providedIn: 'root'
})
export class TerapeutaService {
  
  private apiUrl = `${environment.apiBaseUrl}`;
  
  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  // ============= SESIONES =============

  registrarSesion(sesion: RegistroSesionDTO): Observable<any> {
    const formData = new FormData();
    formData.append('id_nino', sesion.id_nino.toString());
    formData.append('fecha', sesion.fecha);
    formData.append('informacion_clinica', JSON.stringify(sesion.informacionClinica));
    formData.append('informacion_padres', JSON.stringify(sesion.informacionPadres));

    // Adjuntar archivos si existen
    if (sesion.informacionClinica.evidencias) {
      sesion.informacionClinica.evidencias.forEach((file, index) => {
        formData.append(`evidencia_${index}`, file);
      });
    }

    return this.http.post(
      `${this.apiUrl}/terapeuta/sesiones/registrar`,
      formData,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  obtenerSesionesTerapeuta(): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.apiUrl}/terapeuta/sesiones`,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  // ============= ASISTENCIAS =============

  registrarAsistencia(asistencia: AsistenciaDTO): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/terapeuta/asistencias/registrar`,
      asistencia,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  obtenerAsistencias(periodo?: string): Observable<any[]> {
    const params = periodo ? `?periodo=${periodo}` : '';
    return this.http.get<any[]>(
      `${this.apiUrl}/terapeuta/asistencias${params}`,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  reprogramarSesion(reprogramacion: ReprogramacionDTO): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/terapeuta/sesiones/reprogramar`,
      reprogramacion,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  // ============= REPORTES CUATRIMESTRALES =============

  subirReporte(reporte: ReporteDTO): Observable<any> {
    const formData = new FormData();
    formData.append('id_nino', reporte.id_nino.toString());
    formData.append('cuatrimestre', reporte.cuatrimestre);
    formData.append('tipo_reporte', reporte.tipo_reporte);
    formData.append('archivo', reporte.archivo);
    
    if (reporte.observaciones) {
      formData.append('observaciones', reporte.observaciones);
    }

    return this.http.post(
      `${this.apiUrl}/terapeuta/reportes/subir`,
      formData,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  obtenerReportes(idNino?: number): Observable<any[]> {
    const params = idNino ? `?id_nino=${idNino}` : '';
    return this.http.get<any[]>(
      `${this.apiUrl}/terapeuta/reportes${params}`,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  eliminarReporte(idReporte: number): Observable<any> {
    return this.http.delete(
      `${this.apiUrl}/terapeuta/reportes/${idReporte}`,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  // ============= MENSAJERÍA =============

  enviarMensaje(destinatario: string, idDestinatario: number, mensaje: string): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/terapeuta/mensajes/enviar`,
      { tipo_destinatario: destinatario, id_destinatario: idDestinatario, mensaje },
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  obtenerConversaciones(): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.apiUrl}/terapeuta/mensajes/conversaciones`,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  obtenerMensajesConversacion(idConversacion: number): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.apiUrl}/terapeuta/mensajes/conversacion/${idConversacion}`,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  marcarMensajesLeidos(idConversacion: number): Observable<any> {
    return this.http.put(
      `${this.apiUrl}/terapeuta/mensajes/marcar-leidos/${idConversacion}`,
      {},
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  // ============= NIÑOS ASIGNADOS =============

  obtenerNinosAsignados(): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.apiUrl}/terapeuta/ninos`,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  obtenerExpedienteNino(idNino: number): Observable<any> {
    return this.http.get(
      `${this.apiUrl}/terapeuta/ninos/${idNino}/expediente`,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  obtenerHistorialTerapeutico(idNino: number): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.apiUrl}/terapeuta/ninos/${idNino}/historial`,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  // ============= INDICADORES =============

  obtenerIndicadoresDesempeno(): Observable<any> {
    return this.http.get(
      `${this.apiUrl}/terapeuta/indicadores`,
      { headers: this.getHeaders() }
    ).pipe(
      catchError(this.handleError)
    );
  }

  // ============= ERROR HANDLING =============

  private handleError(error: any): Observable<never> {
    console.error('Error en el servicio:', error);
    let errorMessage = 'Ha ocurrido un error en el servidor';

    if (error.error instanceof ErrorEvent) {
      errorMessage = `Error: ${error.error.message}`;
    } else {
      errorMessage = error.error?.message || error.message || errorMessage;
    }

    return throwError(() => new Error(errorMessage));
  }
}

