// src/app/ninos/service/ninos.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment/environment';
import { Nino } from '../interfaces/nino.interface';

@Injectable({
  providedIn: 'root'
})
export class NinosService {

  private baseUrl = `${environment.apiBaseUrl}/ninos`;

  constructor(private http: HttpClient) {}

  obtenerNinoPorId(id: number): Observable<Nino> {
    return this.http.get<Nino>(`${this.baseUrl}/${id}`);
  }

  actualizarNino(id: number, cambios: Partial<Nino>): Observable<Nino> {
    return this.http.put<Nino>(`${this.baseUrl}/${id}`, cambios);
  }
}
