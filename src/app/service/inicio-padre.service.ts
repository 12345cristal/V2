// src/app/padres/service/inicio-padre.service.ts

import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Ajusta la ruta del environment según tu proyecto
import { environment } from '../enviroment/environment';

import { InicioPadreResumen } from '../interfaces/inicio-padre.interface';

@Injectable({
  providedIn: 'root'
})
export class InicioPadreService {

  private http = inject(HttpClient);
  private baseUrl = `${environment.apiBaseUrl}/padres/inicio`;

  /**
   * Obtiene el resumen de inicio para el padre/madre/tutor.
   * Puedes usar el ID del niño, del tutor o deducirlo del token en el backend.
   */
  obtenerResumenInicio(): Observable<InicioPadreResumen> {
    return this.http.get<InicioPadreResumen>(this.baseUrl);
  }
}
