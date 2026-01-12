// src/app/padres/services/inicio.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../enviroment/environment';
import { InicioPadre } from '../../interfaces/padres/inicio.interface';

@Injectable({ providedIn: 'root' })
export class InicioService {

  private readonly baseUrl =
    environment.apiBaseUrl + environment.apiPadresInicio;

  constructor(private http: HttpClient) {}

  obtenerInicio(hijoId?: string) {
    let params = new HttpParams();

    if (hijoId) {
      params = params.set('hijo_id', hijoId);
    }

    return this.http.get<InicioPadre>(this.baseUrl, { params });
  }
}
