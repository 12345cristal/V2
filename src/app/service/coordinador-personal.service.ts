import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';
import { TerapeutaCargaDetalle } from '../interfaces/terapeuta-detalle.interface';

@Injectable({ providedIn: 'root' })
export class CoordinadorPersonalService {
  private base = `${environment.apiBaseUrl}/coordinador`;

  constructor(private http: HttpClient) {}

  getDetalleTerapeuta(idPersonal: number): Observable<TerapeutaCargaDetalle> {
    return this.http.get<TerapeutaCargaDetalle>(
      `${this.base}/personal/${idPersonal}/detalle-carga`
    );
  }
}

