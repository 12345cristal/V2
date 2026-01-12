import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../enviroment/environment';
import { InicioPadre } from '../interfaces/inicio.interface';

@Injectable({
  providedIn: 'root'
})
export class InicioService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiBaseUrl}/padres`;

  obtenerInicio(hijoId?: string): Observable<InicioPadre> {
    const params = hijoId ? `?hijo_id=${hijoId}` : '';
    return this.http.get<InicioPadre>(`${this.baseUrl}/inicio${params}`);
  }
}
