import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { TareaRecurso } from '../../interfaces/inicio-terapeuta.interface';

@Injectable({ providedIn: 'root' })
export class TareasService {
  private api = `${environment.apiBaseUrl}/tareas-recurso`;

  constructor(private http: HttpClient) {}

  /** Tareas asignadas a un niño */
  getTareasPorNino(ninoId: number): Observable<TareaRecurso[]> {
    return this.http.get<TareaRecurso[]>(`${this.api}/nino/${ninoId}`);
  }

  /** Marcar completado / no completado */
  actualizarEstado(tareaId: number, completado: boolean) {
    return this.http.patch(`${this.api}/${tareaId}`, { completado });
  }

  /** Notas del terapeuta */
  actualizarNotasTerapeuta(tareaId: number, notas_terapeuta: string) {
    return this.http.patch(`${this.api}/${tareaId}/notas-terapeuta`, {
      notas_terapeuta,
    });
  }
}
