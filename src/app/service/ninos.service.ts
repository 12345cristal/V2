// src/app/ninos/service/ninos.service.ts

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Nino, EstadoNino } from '../interfaces/nino.interface';
import { environment } from '../enviroment/environment';

@Injectable({
  providedIn: 'root'
})
export class NinosService {

  private baseUrl = `${environment.apiBaseUrl}`;

  constructor(private http: HttpClient) {}

  // ============================================================
  // GET — Lista de niños (con filtros opcionales)
  // ============================================================
  getNinos(options?: { search?: string; estado?: EstadoNino | 'TODOS' }): Observable<Nino[]> {
    let params = new HttpParams();

    if (options?.search) {
      params = params.set('search', options.search);
    }

    if (options?.estado && options.estado !== 'TODOS') {
      params = params.set('estado', options.estado);
    }

    return this.http.get<Nino[]>(this.baseUrl, { params });
  }

  // ============================================================
  // GET — Un niño por ID
  // ============================================================
  getNino(id: number): Observable<Nino> {
    return this.http.get<Nino>(`${this.baseUrl}/${id}`);
  }

  // ============================================================
  // POST — Crear niño (con archivos)
  // ============================================================
  createNino(payload: {
    nino: Nino;
    archivos?: {
      actaNacimiento?: File | null;
      curp?: File | null;
      comprobanteDomicilio?: File | null;
      foto?: File | null;
      diagnostico?: File | null;
      consentimiento?: File | null;
      hojaIngreso?: File | null;
    };
  }): Observable<Nino> {

    const formData = this.toFormData(payload);
    return this.http.post<Nino>(this.baseUrl, formData);
  }

  // ============================================================
  // PUT — Actualizar niño (con archivos)
  // ============================================================
  updateNino(
    id: number,
    payload: {
      nino: Nino;
      archivos?: {
        actaNacimiento?: File | null;
        curp?: File | null;
        comprobanteDomicilio?: File | null;
        foto?: File | null;
        diagnostico?: File | null;
        consentimiento?: File | null;
        hojaIngreso?: File | null;
      };
    }
  ): Observable<Nino> {

    const formData = this.toFormData(payload);
    return this.http.put<Nino>(`${this.baseUrl}/${id}`, formData);
  }

  // ============================================================
  // PATCH — Cambiar estado del niño
  // ============================================================
  cambiarEstado(id: number, estado: EstadoNino): Observable<Nino> {
    return this.http.patch<Nino>(`${this.baseUrl}/${id}/estado`, { estado });
  }


  // ============================================================
  // HELPERS — FormData
  // ============================================================
  private toFormData(payload: {
    nino: Nino;
    archivos?: { [k: string]: File | null | undefined };
  }): FormData {

    const fd = new FormData();

    // El backend recibe JSON dentro del form-data
    fd.append('nino', JSON.stringify(payload.nino));

    if (payload.archivos) {
      Object.entries(payload.archivos).forEach(([key, file]) => {
        if (file) {
          fd.append(key, file);
        }
      });
    }

    return fd;
  }
}
