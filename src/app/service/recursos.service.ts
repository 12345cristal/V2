// src/app/service/recursos.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../enviroment/environment';
import {
  Recurso,
  RecursoListItem,
  RecursoCreate,
  RecursoUpdate,
  TipoRecurso,
  CategoriaRecurso,
  NivelRecurso
} from '../interfaces/recurso.interface';

@Injectable({
  providedIn: 'root'
})
export class RecursosService {
  private apiUrl = `${environment.apiBaseUrl}/recursos`;

  constructor(private http: HttpClient) {}

  // Catálogos
  getTipos(): Observable<TipoRecurso[]> {
    return this.http.get<TipoRecurso[]>(`${this.apiUrl}/tipos`);
  }

  getCategorias(): Observable<CategoriaRecurso[]> {
    return this.http.get<CategoriaRecurso[]>(`${this.apiUrl}/categorias`);
  }

  getNiveles(): Observable<NivelRecurso[]> {
    return this.http.get<NivelRecurso[]>(`${this.apiUrl}/niveles`);
  }

  // CRUD Recursos
  listar(filtros?: {
    activo?: number;
    tipoId?: number;
    categoriaId?: number;
    nivelId?: number;
    destacado?: number;
    busqueda?: string;
    skip?: number;
    limit?: number;
  }): Observable<RecursoListItem[]> {
    let params = new HttpParams();
    if (filtros) {
      if (filtros.activo !== undefined) params = params.set('activo', filtros.activo.toString());
      if (filtros.tipoId) params = params.set('tipo_id', filtros.tipoId.toString());
      if (filtros.categoriaId) params = params.set('categoria_id', filtros.categoriaId.toString());
      if (filtros.nivelId) params = params.set('nivel_id', filtros.nivelId.toString());
      if (filtros.destacado !== undefined) params = params.set('destacado', filtros.destacado.toString());
      if (filtros.busqueda) params = params.set('busqueda', filtros.busqueda);
      if (filtros.skip) params = params.set('skip', filtros.skip.toString());
      if (filtros.limit) params = params.set('limit', filtros.limit.toString());
    }
    return this.http.get<RecursoListItem[]>(this.apiUrl, { params });
  }

  obtener(id: number): Observable<Recurso> {
    return this.http.get<Recurso>(`${this.apiUrl}/${id}`);
  }

  crear(recurso: RecursoCreate): Observable<Recurso> {
    return this.http.post<Recurso>(this.apiUrl, recurso);
  }

  actualizar(id: number, recurso: RecursoUpdate): Observable<Recurso> {
    return this.http.put<Recurso>(`${this.apiUrl}/${id}`, recurso);
  }

  eliminar(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  listarDestacados(limite: number = 10): Observable<RecursoListItem[]> {
    const params = new HttpParams().set('limite', limite.toString());
    return this.http.get<RecursoListItem[]>(`${this.apiUrl}/destacados/listar`, { params });
  }
}
