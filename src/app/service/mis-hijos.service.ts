import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Hijo } from '../interfaces/hijo.interface';

export type HijoCreateDto = Omit<Hijo, 'id'>;
export type HijoUpdateDto = Partial<Omit<Hijo, 'id'>>;

@Injectable({ providedIn: 'root' })
export class MisHijosService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiBaseUrl}/padre/hijos`;

  getHijos(): Observable<Hijo[]> {
    return this.http.get<Hijo[]>(this.baseUrl);
  }

  getHijo(id: number): Observable<Hijo> {
    return this.http.get<Hijo>(`${this.baseUrl}/${id}`);
  }

  createHijo(payload: HijoCreateDto): Observable<Hijo> {
    return this.http.post<Hijo>(this.baseUrl, payload);
  }

  updateHijo(id: number, payload: HijoUpdateDto): Observable<Hijo> {
    return this.http.put<Hijo>(`${this.baseUrl}/${id}`, payload);
  }

  deleteHijo(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}

