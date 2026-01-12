import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  InicioPage,
  MisHijosPage,
  SesionesPage,
  HistorialTerapeuticoPage,
  TareasPage,
  PagosPage,
  DocumentosPage,
  RecursosPage,
  MensajesPage,
  NotificacionesPage,
  PerfilPage,
  Hijo,
  Sesion,
  Tarea,
  Documento,
  Mensaje,
  Chat,
  Notificacion,
  RespuestaApi,
  ListadoPaginado
} from './padres.interfaces';

@Injectable({
  providedIn: 'root'
})
export class PadresService {
  private apiUrl = '/api/padres';

  constructor(private http: HttpClient) {}

  // ========================================================================
  // 1️⃣ INICIO
  // ========================================================================
  getInicioData(): Observable<RespuestaApi<InicioPage>> {
    return this.http.get<RespuestaApi<InicioPage>>(`${this.apiUrl}/inicio`);
  }

  // ========================================================================
  // 2️⃣ MIS HIJOS
  // ========================================================================
  getMisHijos(): Observable<RespuestaApi<MisHijosPage>> {
    return this.http.get<RespuestaApi<MisHijosPage>>(`${this.apiUrl}/mis-hijos`);
  }

  getHijoDetalle(hijoId: string): Observable<RespuestaApi<Hijo>> {
    return this.http.get<RespuestaApi<Hijo>>(`${this.apiUrl}/mis-hijos/${hijoId}`);
  }

  // ========================================================================
  // 3️⃣ SESIONES
  // ========================================================================
  getSesiones(filtro?: 'hoy' | 'programadas' | 'semana'): Observable<RespuestaApi<SesionesPage>> {
    const params = filtro ? `?filtro=${filtro}` : '';
    return this.http.get<RespuestaApi<SesionesPage>>(`${this.apiUrl}/sesiones${params}`);
  }

  getSesionDetalle(sesionId: string): Observable<RespuestaApi<Sesion>> {
    return this.http.get<RespuestaApi<Sesion>>(`${this.apiUrl}/sesiones/${sesionId}`);
  }

  descargarBitacora(sesionId: string): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/sesiones/${sesionId}/bitacora`, {
      responseType: 'blob'
    });
  }

  // ========================================================================
  // 4️⃣ HISTORIAL TERAPÉUTICO
  // ========================================================================
  getHistorialTerapeutico(): Observable<RespuestaApi<HistorialTerapeuticoPage>> {
    return this.http.get<RespuestaApi<HistorialTerapeuticoPage>>(`${this.apiUrl}/historial-terapeutico`);
  }

  descargarReporteTerapeutico(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/historial-terapeutico/reporte`, {
      responseType: 'blob'
    });
  }

  descargarResumenMensual(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/historial-terapeutico/resumen-mensual`, {
      responseType: 'blob'
    });
  }

  // ========================================================================
  // 5️⃣ TAREAS
  // ========================================================================
  getTareas(filtro?: 'todas' | 'pendientes' | 'realizadas' | 'vencidas'): Observable<RespuestaApi<TareasPage>> {
    const params = filtro ? `?filtro=${filtro}` : '';
    return this.http.get<RespuestaApi<TareasPage>>(`${this.apiUrl}/tareas${params}`);
  }

  completarTarea(tareaId: string): Observable<RespuestaApi<Tarea>> {
    return this.http.put<RespuestaApi<Tarea>>(`${this.apiUrl}/tareas/${tareaId}/completar`, {});
  }

  // ========================================================================
  // 6️⃣ PAGOS
  // ========================================================================
  getPagos(): Observable<RespuestaApi<PagosPage>> {
    return this.http.get<RespuestaApi<PagosPage>>(`${this.apiUrl}/pagos`);
  }

  descargarReportePagos(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/pagos/reporte`, {
      responseType: 'blob'
    });
  }

  descargarComprobante(pagoId: string): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/pagos/${pagoId}/comprobante`, {
      responseType: 'blob'
    });
  }

  // ========================================================================
  // 7️⃣ DOCUMENTOS
  // ========================================================================
  getDocumentos(): Observable<RespuestaApi<DocumentosPage>> {
    return this.http.get<RespuestaApi<DocumentosPage>>(`${this.apiUrl}/documentos`);
  }

  marcarDocumentoVisto(documentoId: string): Observable<RespuestaApi<Documento>> {
    return this.http.put<RespuestaApi<Documento>>(
      `${this.apiUrl}/documentos/${documentoId}/visto`,
      {}
    );
  }

  descargarDocumento(documentoId: string): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/documentos/${documentoId}/pdf`, {
      responseType: 'blob'
    });
  }

  // ========================================================================
  // 8️⃣ RECURSOS RECOMENDADOS
  // ========================================================================
  getRecursos(): Observable<RespuestaApi<RecursosPage>> {
    return this.http.get<RespuestaApi<RecursosPage>>(`${this.apiUrl}/recursos`);
  }

  marcarRecursoVisto(recursoId: string): Observable<RespuestaApi<any>> {
    return this.http.put<RespuestaApi<any>>(
      `${this.apiUrl}/recursos/${recursoId}/visto`,
      {}
    );
  }

  // ========================================================================
  // 9️⃣ MENSAJES
  // ========================================================================
  getMensajes(): Observable<RespuestaApi<MensajesPage>> {
    return this.http.get<RespuestaApi<MensajesPage>>(`${this.apiUrl}/mensajes`);
  }

  getChat(contactoId: string): Observable<RespuestaApi<Chat>> {
    return this.http.get<RespuestaApi<Chat>>(`${this.apiUrl}/mensajes/chat/${contactoId}`);
  }

  enviarMensaje(contactoId: string, contenido: string, tipo: 'texto' | 'audio' | 'archivo' = 'texto'): Observable<RespuestaApi<Mensaje>> {
    return this.http.post<RespuestaApi<Mensaje>>(
      `${this.apiUrl}/mensajes/enviar`,
      { contactoId, contenido, tipo }
    );
  }

  // ========================================================================
  // 🔔 10️⃣ NOTIFICACIONES
  // ========================================================================
  getNotificaciones(): Observable<RespuestaApi<NotificacionesPage>> {
    return this.http.get<RespuestaApi<NotificacionesPage>>(`${this.apiUrl}/notificaciones`);
  }

  marcarNotificacionLeida(notificacionId: string): Observable<RespuestaApi<Notificacion>> {
    return this.http.put<RespuestaApi<Notificacion>>(
      `${this.apiUrl}/notificaciones/${notificacionId}/leer`,
      {}
    );
  }

  marcarTodasLargasNotificacionesLeidas(): Observable<RespuestaApi<any>> {
    return this.http.put<RespuestaApi<any>>(
      `${this.apiUrl}/notificaciones/marcar-todas-leidas`,
      {}
    );
  }

  // ========================================================================
  // ⚙️ 11️⃣ PERFIL Y ACCESIBILIDAD
  // ========================================================================
  getPerfil(): Observable<RespuestaApi<PerfilPage>> {
    return this.http.get<RespuestaApi<PerfilPage>>(`${this.apiUrl}/perfil`);
  }

  actualizarPreferenciasAccesibilidad(preferencias: any): Observable<RespuestaApi<PerfilPage>> {
    return this.http.put<RespuestaApi<PerfilPage>>(
      `${this.apiUrl}/perfil/accesibilidad`,
      preferencias
    );
  }

  actualizarPerfilUsuario(datos: any): Observable<RespuestaApi<PerfilPage>> {
    return this.http.put<RespuestaApi<PerfilPage>>(
      `${this.apiUrl}/perfil`,
      datos
    );
  }
}
