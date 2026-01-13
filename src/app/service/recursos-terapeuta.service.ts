// src/app/service/recursos-terapeuta.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

/* ===========================
   INTERFACES
=========================== */
export interface Recurso {
  id: number;
  titulo: string;
  descripcion: string;
  tipo_recurso: 'PDF' | 'VIDEO' | 'ENLACE';
  categoria_recurso: string;
  nivel_recurso: string;
  url: string;
  archivo: string | null;
  objetivo_terapeutico: string;
  fecha_creacion: string;
  asignaciones: number;
}

export interface Hijo {
  id: number;
  nombre: string;
  apellido: string;
  edad: number;
  padre_nombre: string;
  padre_id: number;
}

export interface RecursoCreacionResponse {
  message: string;
  id: number;
}

export interface RecursoEliminacionResponse {
  message: string;
}

/* ===========================
   SERVICE
=========================== */
@Injectable({
  providedIn: 'root'
})
export class RecursosTerapeutaService {

  private readonly apiUrl =
    `${environment.apiBaseUrl}/recursos`;

  private readonly terapeutasUrl =
    `${environment.apiBaseUrl}/terapeutas`;

  constructor(private http: HttpClient) {}

  /* ===========================
     RECURSOS
  =========================== */

  obtenerMisRecursos(): Observable<Recurso[]> {
    return this.http.get<Recurso[]>(`${this.apiUrl}/mis-recursos`);
  }

  crearRecurso(formData: FormData): Observable<RecursoCreacionResponse> {
    return this.http.post<RecursoCreacionResponse>(
      this.apiUrl,
      formData
    );
  }

  actualizarRecurso(
    id: number,
    formData: FormData
  ): Observable<RecursoCreacionResponse> {
    return this.http.put<RecursoCreacionResponse>(
      `${this.apiUrl}/${id}`,
      formData
    );
  }

  eliminarRecurso(id: number): Observable<RecursoEliminacionResponse> {
    return this.http.delete<RecursoEliminacionResponse>(
      `${this.apiUrl}/${id}`
    );
  }

  /* ===========================
     ✅ DESCARGA DE ARCHIVO
  =========================== */
  descargarRecurso(rutaArchivo: string | null): void {
    if (!rutaArchivo) return;

    const link = document.createElement('a');
    link.href = rutaArchivo;
    link.download = rutaArchivo.split('/').pop() ?? 'recurso';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  /* ===========================
     TERAPEUTA / PACIENTES
  =========================== */

  obtenerHijosPacientes(): Observable<Hijo[]> {
    return this.http.get<Hijo[]>(
      `${this.terapeutasUrl}/mis-pacientes`
    );
  }

  obtenerPerfilTerapeuta(): Observable<any> {
    return this.http.get(`${this.terapeutasUrl}/perfil`);
  }
}
