import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { TareaPadre } from '../interfaces/tarea.interface';

@Injectable({ providedIn: 'root' })
export class TareasPadreService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiBaseUrl}/padre/tareas`;

  getTareas(hijoId: number): Observable<TareaPadre[]> {
    return this.http.get<TareaPadre[]>(`${this.baseUrl}/${hijoId}`);
  }

  marcarRealizada(
    tareaId: number,
    observaciones?: string,
    evidencia?: File
  ): Observable<TareaPadre> {
    const formData = new FormData();
    
    if (observaciones) {
      formData.append('observaciones', observaciones);
    }
    
    if (evidencia) {
      formData.append('evidencia', evidencia);
    }

    return this.http.put<TareaPadre>(
      `${this.baseUrl}/${tareaId}/marcar-realizada`,
      formData
    );
  }

  descargarRecurso(url: string): Observable<Blob> {
    return this.http.get(url, { responseType: 'blob' });
  }
}




