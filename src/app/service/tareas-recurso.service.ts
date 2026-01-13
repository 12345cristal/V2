// src/app/service/tareas-recurso.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  TareaRecurso,
  TareaRecursoListItem,
  TareaRecursoCreate,
  TareaRecursoUpdate,
  EstadisticasTareas
} from '../interfaces/tarea-recurso.interface';

@Injectable({
  providedIn: 'root'
})
export class TareasRecursoService {
  private apiUrl = `${environment.apiBaseUrl}/tareas-recurso`;

  constructor(private http: HttpClient) {}

  listarPorNino(
    ninoId: number,
    filtros?: {
      completado?: number;
      vencidas?: boolean;
      skip?: number;
      limit?: number;
    }
  ): Observable<TareaRecursoListItem[]> {
    let params = new HttpParams();
    if (filtros) {
      if (filtros.completado !== undefined) params = params.set('completado', filtros.completado.toString());
      if (filtros.vencidas !== undefined) params = params.set('vencidas', filtros.vencidas.toString());
      if (filtros.skip) params = params.set('skip', filtros.skip.toString());
      if (filtros.limit) params = params.set('limit', filtros.limit.toString());
    }
    return this.http.get<TareaRecursoListItem[]>(`${this.apiUrl}/nino/${ninoId}`, { params });
  }

  obtener(tareaId: number): Observable<TareaRecurso> {
    return this.http.get<TareaRecurso>(`${this.apiUrl}/${tareaId}`);
  }

  crear(tarea: TareaRecursoCreate): Observable<TareaRecurso> {
    return this.http.post<TareaRecurso>(this.apiUrl, tarea);
  }

  actualizar(tareaId: number, tarea: TareaRecursoUpdate): Observable<TareaRecurso> {
    return this.http.put<TareaRecurso>(`${this.apiUrl}/${tareaId}`, tarea);
  }

  marcarCompletada(
    tareaId: number,
    comentariosPadres?: string,
    evidencia?: File
  ): Observable<TareaRecurso> {
    const formData = new FormData();
    if (comentariosPadres) {
      formData.append('comentarios_padres', comentariosPadres);
    }
    if (evidencia) {
      formData.append('evidencia', evidencia);
    }
    return this.http.post<TareaRecurso>(`${this.apiUrl}/${tareaId}/completar`, formData);
  }

  eliminar(tareaId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${tareaId}`);
  }

  obtenerEstadisticas(ninoId: number): Observable<EstadisticasTareas> {
    return this.http.get<EstadisticasTareas>(`${this.apiUrl}/nino/${ninoId}/estadisticas`);
  }
}




