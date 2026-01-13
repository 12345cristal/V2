import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { HistorialResumen } from '../interfaces/historial.interface';

@Injectable({ providedIn: 'root' })
export class HistorialPadreService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiBaseUrl}/padre/historial`;

  getResumen(hijoId: number): Observable<HistorialResumen> {
    return this.http.get<HistorialResumen>(`${this.baseUrl}/${hijoId}`);
  }

  descargarReporte(hijoId: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/${hijoId}/reporte`, {
      responseType: 'blob'
    });
  }
}

