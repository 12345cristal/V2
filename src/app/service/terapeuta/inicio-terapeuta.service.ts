import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Cita } from '../../interfaces/terapeuta/cita.interface';

export interface TerapeutaDashboard {
  resumen: {
    total_ninos: number;
    citas_hoy: number;
    citas_semana: number;
    tareas_pendientes: number;
    recursos_nuevos: number;
  };
  proximas_citas: CitaExtendida[];
  ninos: NinoMini[];
}

export interface NinoMini {
  id: number;
  nombre: string;
  apellido_paterno: string;
  estado: 'ACTIVO' | 'BAJA_TEMPORAL' | 'INACTIVO';
}

export interface CitaExtendida extends Cita {
  nino_nombre: string;
  terapia_nombre: string;
}

@Injectable({ providedIn: 'root' })
export class InicioTerapeutaService {
  private readonly api = `${environment.apiBaseUrl}/terapeuta/dashboard`;

  constructor(private http: HttpClient) {}

  /** Dashboard completo */
  getDashboard(): Observable<TerapeutaDashboard> {
    return this.http.get<TerapeutaDashboard>(this.api);
  }

  /** Próximas citas por rango (opcional, por si quieres recargar solo calendario) */
  getProximasCitas(desde: string, hasta: string): Observable<CitaExtendida[]> {
    const params = new HttpParams().set('desde', desde).set('hasta', hasta);
    return this.http.get<CitaExtendida[]>(`${this.api}/citas`, { params });
  }
}
