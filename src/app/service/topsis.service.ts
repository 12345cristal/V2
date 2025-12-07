import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../enviroment/environment';
import { TopsisRequest, TopsisResultado } from '../interfaces/topsis.interface';

@Injectable({ providedIn: 'root' })
export class TopsisService {

  private api = `${environment.apiBaseUrl}/coordinador/topsis`;

  constructor(private http: HttpClient) {}

  calcularPersonalizado(body: TopsisRequest): Observable<TopsisResultado[]> {
    return this.http.post<TopsisResultado[]>(`${this.api}/terapeutas/custom`, body);
  }

  obtenerAutomatico() {
    return this.http.get(`${this.api}/terapeutas`);
  }
}
