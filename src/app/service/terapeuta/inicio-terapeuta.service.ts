import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Cita } from '../../interfaces/terapeuta/cita.interface';
import { ModuloTerapeuta, ModuloEstado, DashboardModulos } from '../../interfaces/terapeuta/modulos.interface';

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
  modulos?: ModuloTerapeuta[];
  estados_modulos?: ModuloEstado[];
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
  private readonly modulosApi = `${environment.apiBaseUrl}/terapeuta/modulos`;

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

  /** Obtener todos los módulos disponibles */
  getModulos(): Observable<ModuloTerapeuta[]> {
    return this.http.get<ModuloTerapeuta[]>(this.modulosApi);
  }

  /** Obtener estado de los módulos */
  getEstadosModulos(): Observable<ModuloEstado[]> {
    return this.http.get<ModuloEstado[]>(`${this.modulosApi}/estados`);
  }

  /** Obtener información completa de módulos */
  getDashboardModulos(): Observable<DashboardModulos> {
    return this.http.get<DashboardModulos>(`${this.modulosApi}/dashboard`);
  }
}
