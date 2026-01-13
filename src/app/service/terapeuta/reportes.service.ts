import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Reporte } from '../../interfaces/terapeuta/reporte.interface';

@Injectable({ providedIn: 'root' })
export class ReportesService {

  private readonly api = `${environment.apiBaseUrl}/terapeuta/reportes`;

  constructor(private http: HttpClient) {}

  /**
   * Reportes de un niño
   */
  getReportesPorNino(ninoId: number): Observable<Reporte[]> {
    return this.http.get<Reporte[]>(`${this.api}/nino/${ninoId}`);
  }

  /**
   * Crear reporte por sesión
   */
  crearReporteSesion(payload: {
    nino_id: number;
    sesion_id: number;
    observaciones: string;
  }): Observable<Reporte> {
    return this.http.post<Reporte>(`${this.api}/sesion`, payload);
  }

  /**
   * Crear reporte cuatrimestral
   */
  crearReporteCuatrimestral(payload: {
    nino_id: number;
    periodo_inicio: string;
    periodo_fin: string;
    observaciones: string;
  }): Observable<Reporte> {
    return this.http.post<Reporte>(
      `${this.api}/cuatrimestral`,
      payload
    );
  }

}
