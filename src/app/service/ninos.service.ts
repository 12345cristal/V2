// ninos.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Nino, EstadoNino } from '../interfaces/nino.interface';

@Injectable({
  providedIn: 'root'
})
export class NinosService {

  private api = 'http://localhost:8000/ninos';

  constructor(private http: HttpClient) {}

  getNinos(options?: { search?: string; estado?: EstadoNino | 'TODOS' }): Observable<Nino[]> {
    let params = new HttpParams();
    if (options?.search) params = params.set('search', options.search);
    if (options?.estado && options.estado !== 'TODOS') {
      params = params.set('estado', options.estado);
    }
    return this.http.get<Nino[]>(this.api, { params });
  }

  getNino(id: number): Observable<Nino> {
    return this.http.get<Nino>(`${this.api}/${id}`);
  }

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
    return this.http.post<Nino>(this.api, formData);
  }

  updateNino(id: number, payload: {
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
    return this.http.put<Nino>(`${this.api}/${id}`, formData);
  }

  cambiarEstado(id: number, estado: EstadoNino): Observable<Nino> {
    return this.http.patch<Nino>(`${this.api}/${id}/estado`, { estado });
  }

  // ===================== helpers =====================
  private toFormData(payload: {
    nino: Nino;
    archivos?: { [k: string]: File | null | undefined };
  }): FormData {
    const fd = new FormData();
    fd.append('nino', JSON.stringify(payload.nino));

    if (payload.archivos) {
      Object.entries(payload.archivos).forEach(([key, file]) => {
        if (file) fd.append(key, file);
      });
    }
    return fd;
  }
}
