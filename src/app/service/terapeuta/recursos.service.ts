import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Recurso } from '../../interfaces/terapeuta/recurso.interface';

@Injectable({ providedIn: 'root' })
export class RecursosService {

  private readonly api = `${environment.apiBaseUrl}/recursos`;

  constructor(private http: HttpClient) {}

  /**
   * Recursos globales (libros, videos, pdf)
   */
  getRecursos(): Observable<Recurso[]> {
    return this.http.get<Recurso[]>(this.api);
  }

  /**
   * Subir recurso (archivo + metadata)
   */
  crearRecurso(formData: FormData): Observable<Recurso> {
    return this.http.post<Recurso>(this.api, formData);
  }

  /**
   * Asignar recurso como tarea a un niño
   */
  asignarRecursoANino(payload: {
    recurso_id: number;
    nino_id: number;
    fecha_limite?: string;
  }): Observable<any> {
    return this.http.post(
      `${environment.apiBaseUrl}/tareas-recurso`,
      payload
    );
  }

}
