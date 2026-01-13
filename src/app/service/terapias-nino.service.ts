// src/app/padre/terapias/services/terapias-nino.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import {
  NinoTerapiasDetalle,
  TerapiaAsignadaNino
} from '../interfaces/terapias-nino.interface';

import { environment } from '../environment/environment';

@Injectable({
  providedIn: 'root'
})
export class TerapiasNinoService {

  private readonly baseUrl = environment.apiBaseUrl; // ✔ Ahora viene del environment

  constructor(private http: HttpClient) {}

  /**
   * Obtiene el resumen del niño + terapias asignadas.
   * GET /ninos/{id}/terapias
   */
  obtenerTerapiasDeNino(idNino: number): Observable<NinoTerapiasDetalle> {
    return this.http.get<NinoTerapiasDetalle>(
      `${this.baseUrl}/ninos/${idNino}/terapias`
    );
  }

  /**
   * Solo listado de terapias asignadas al niño.
   * GET /ninos/{id}/terapias/listado
   */
  obtenerSoloTerapiasDeNino(idNino: number): Observable<TerapiaAsignadaNino[]> {
    return this.http.get<TerapiaAsignadaNino[]>(
      `${this.baseUrl}/ninos/${idNino}/terapias/listado`
    );
  }
}
