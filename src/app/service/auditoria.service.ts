import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../enviroment/environment';
import { RegistroAuditoria } from '../interfaces/auditoria.interface';

@Injectable({ providedIn: 'root' })
export class AuditoriaService {
  private base = `${environment.apiBaseUrl}/auditoria`;

  constructor(private http: HttpClient) {}

  buscar(options: {
    fechaDesde?: string;
    fechaHasta?: string;
    usuario?: string;
    modulo?: string;
    accion?: string;
  }): Observable<RegistroAuditoria[]> {
    let params = new HttpParams();

    if (options.fechaDesde) params = params.set('fecha_desde', options.fechaDesde);
    if (options.fechaHasta) params = params.set('fecha_hasta', options.fechaHasta);
    if (options.usuario)    params = params.set('usuario', options.usuario);
    if (options.modulo)     params = params.set('modulo', options.modulo);
    if (options.accion)     params = params.set('accion', options.accion);

    return this.http.get<RegistroAuditoria[]>(this.base, { params });
  }
}
