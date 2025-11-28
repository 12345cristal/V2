import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../enviroment/environment';

import {
  RecursoTerapeuta,
  CrearRecursoDto,
  ActualizarRecursoDto,
  NinoResumen,
  TareaAsignada,
  CrearTareaDto,
  ActualizarTareaDto,
  FiltrosRecurso
} from '../interfaces/recurso-terapeuta.interface';

@Injectable({
  providedIn: 'root'
})
export class RecursosTerapeutaService {

  private readonly baseUrl = `${environment.apiBaseUrl}/terapeuta/recursos`;

  constructor(private http: HttpClient) {}

  // 🔹 Filtros (tipos, categorías, niveles, estados) desde BD
  getFiltros(): Observable<FiltrosRecurso> {
    return this.http.get<FiltrosRecurso>(`${this.baseUrl}/filtros`);
  }

  // 🔹 Recursos (listado con filtros)
  getRecursos(filtros?: {
    texto?: string;
    categoriaId?: string;
    estadoId?: string;
  }): Observable<RecursoTerapeuta[]> {
    let params = new HttpParams();

    if (filtros?.texto) {
      params = params.set('texto', filtros.texto);
    }
    if (filtros?.categoriaId && filtros.categoriaId !== 'todos') {
      params = params.set('categoriaId', filtros.categoriaId);
    }
    if (filtros?.estadoId && filtros.estadoId !== 'todos') {
      params = params.set('estadoId', filtros.estadoId);
    }

    return this.http.get<RecursoTerapeuta[]>(this.baseUrl, { params });
  }

  // 🔹 Recursos destacados
  getRecursosDestacados(): Observable<RecursoTerapeuta[]> {
    return this.http.get<RecursoTerapeuta[]>(`${this.baseUrl}/destacados`);
  }

  // 🔹 CRUD de recursos
  crearRecurso(data: CrearRecursoDto): Observable<RecursoTerapeuta> {
    return this.http.post<RecursoTerapeuta>(this.baseUrl, data);
  }

  actualizarRecurso(id: number, data: ActualizarRecursoDto): Observable<RecursoTerapeuta> {
    return this.http.put<RecursoTerapeuta>(`${this.baseUrl}/${id}`, data);
  }

  eliminarRecurso(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }

  // 🔹 Niños disponibles para asignar tareas
  getNinosAsignables(): Observable<NinoResumen[]> {
    return this.http.get<NinoResumen[]>(`${environment.apiBaseUrl}/terapeuta/ninos`);
  }

  // 🔹 Tareas por recurso
  getTareasPorRecurso(recursoId: number): Observable<TareaAsignada[]> {
    return this.http.get<TareaAsignada[]>(`${this.baseUrl}/${recursoId}/tareas`);
  }

  crearTareas(dto: CrearTareaDto): Observable<void> {
    // El recursoId viene en el DTO
    return this.http.post<void>(`${this.baseUrl}/${dto.recursoId}/tareas`, dto);
  }

  actualizarTarea(tareaId: number, dto: ActualizarTareaDto): Observable<TareaAsignada> {
    return this.http.patch<TareaAsignada>(`${this.baseUrl}/tareas/${tareaId}`, dto);
  }
}
