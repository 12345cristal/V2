import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
interface Recurso {
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

interface Hijo {
  id: number;
  nombre: string;
  apellido: string;
  edad: number;
  padre_nombre: string;
  padre_id: number;
}

interface RecursoCreacionResponse {
  message: string;
  id: number;
}

interface RecursoEliminacionResponse {
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class RecursosTerapeutaService {
  private readonly apiUrl = `${environment.apiUrl}/recursos`;
  private readonly terapeutasUrl = `${environment.apiUrl}/terapeutas`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene todos los recursos creados por el terapeuta actual
   */
  obtenerMisRecursos(): Observable<Recurso[]> {
    return this.http.get<Recurso[]>(`${this.apiUrl}/mis-recursos`);
  }

  /**
   * Obtiene la lista de hijos/pacientes asignados al terapeuta
   */
  obtenerHijosPacientes(): Observable<Hijo[]> {
    return this.http.get<Hijo[]>(`${this.terapeutasUrl}/mis-pacientes`);
  }

  /**
   * Crea un nuevo recurso con archivo o URL
   */
  crearRecurso(formData: FormData): Observable<RecursoCreacionResponse> {
    return this.http.post<RecursoCreacionResponse>(`${this.apiUrl}`, formData);
  }

  /**
   * Actualiza un recurso existente
   */
  actualizarRecurso(
    id: number,
    formData: FormData
  ): Observable<RecursoCreacionResponse> {
    return this.http.put<RecursoCreacionResponse>(
      `${this.apiUrl}/${id}`,
      formData
    );
  }

  /**
   * Elimina un recurso (solo si lo creó el terapeuta actual)
   */
  eliminarRecurso(id: number): Observable<RecursoEliminacionResponse> {
    return this.http.delete<RecursoEliminacionResponse>(`${this.apiUrl}/${id}`);
  }

  /**
   * Descarga un archivo de recurso
   */
  descargarRecurso(rutaArchivo: string): void {
    const link = document.createElement('a');
    link.href = rutaArchivo;
    link.download = rutaArchivo.split('/').pop() || 'descarga';
    link.click();
  }

  /**
   * Obtiene un recurso específico por ID
   */
  obtenerRecurso(id: number): Observable<Recurso> {
    return this.http.get<Recurso>(`${this.apiUrl}/${id}`);
  }

  /**
   * Obtiene los detalles completos de un paciente
   */
  obtenerDetallePaciente(hijoId: number): Observable<any> {
    return this.http.get(`${this.terapeutasUrl}/paciente/${hijoId}`);
  }

  /**
   * Obtiene las estadísticas de un paciente en un período
   */
  obtenerEstadisticasPaciente(
    hijoId: number,
    periodo: string = 'mes'
  ): Observable<any> {
    return this.http.get(
      `${this.terapeutasUrl}/paciente/${hijoId}/estadisticas?periodo=${periodo}`
    );
  }

  /**
   * Obtiene el perfil del terapeuta actual
   */
  obtenerPerfilTerapeuta(): Observable<any> {
    return this.http.get(`${this.terapeutasUrl}/perfil`);
  }

  /**
   * Asigna un nuevo paciente al terapeuta
   */
  asignarPaciente(hijoId: number): Observable<any> {
    return this.http.post(`${this.terapeutasUrl}/paciente/${hijoId}/asignar`, {});
  }

  /**
   * Desasigna un paciente del terapeuta
   */
  desasignarPaciente(hijoId: number): Observable<any> {
    return this.http.delete(
      `${this.terapeutasUrl}/paciente/${hijoId}/desasignar`
    );
  }
}




