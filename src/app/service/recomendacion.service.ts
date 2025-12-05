import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../enviroment/environment';
import { Observable } from 'rxjs';

export interface RecursoRecomendado {
  id: number;
  titulo: string;
  descripcion?: string;
  score: number;
}

@Injectable({ providedIn: 'root' })
export class RecomendacionService {
  private base = `${environment.apiBaseUrl}/padres`;

  constructor(private http: HttpClient) {}

  obtenerRecomendaciones(idNino: number): Observable<RecursoRecomendado[]> {
    return this.http.get<RecursoRecomendado[]>(
      `${this.base}/${idNino}/recomendaciones`
    );
  }
}
