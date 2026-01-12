import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Personal, Rol, EstadoLaboral, HorarioPersonal } from '../interfaces/personal.interface';
import { environment } from '../environments/environment';

export interface NinoAsignado {
  id_terapia_nino: number;
  id_nino: number;
  nombre_completo: string;
  foto: string | null;
  terapia_nombre: string;
  terapia_categoria: string;
  fecha_asignacion: string | null;
  activo: boolean;
  total_sesiones: number;
}

export interface SesionRegistro {
  id_sesion: number;
  fecha: string;
  id_nino: number;
  nombre_nino: string;
  foto_nino: string | null;
  terapia_nombre: string;
  asistio: boolean;
  progreso: number | null;
  colaboracion: number | null;
  observaciones: string;
  creado_por: number | null;
}

export interface DatosCompletosPersonal {
  id_personal: number;
  nombre_completo: string;
  horarios: HorarioPersonal[];
  ninos_asignados: NinoAsignado[];
  sesiones: SesionRegistro[];
  total_ninos: number;
  total_sesiones: number;
}

interface PersonalBackendResponse {
  id_personal: number;
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string;
  id_rol: number;
  especialidad_principal: string;
  telefono_personal: string;
  correo_personal: string;
  fecha_ingreso: string;
  fecha_nacimiento: string;
  estado_laboral: EstadoLaboral;
  total_pacientes: number;
  sesiones_semana: number;
  rating: number | null;
  grado_academico?: string;
  especialidades?: string;
  rfc: string;
  ine?: string;
  curp: string;
  domicilio_calle: string;
  domicilio_colonia: string;
  domicilio_cp: string;
  domicilio_municipio: string;
  domicilio_estado: string;
  cv_archivo?: string;
  foto_url?: string;
  experiencia: string;
  horarios?: any[];
}

interface PersonalListResponse {
  items: PersonalBackendResponse[];
  total: number;
  page: number;
  page_size: number;
}

@Injectable({
  providedIn: 'root'
})
export class PersonalService {
  private baseUrl = `${environment.apiBaseUrl}/personal`;

  constructor(private http: HttpClient) {}

  // ===== ROLES =====
  getRoles(): Observable<Rol[]> {
    return this.http.get<Rol[]>(`${this.baseUrl}/roles/`);
  }

  // ===== PERSONAL =====
  getPersonal(options?: {
    search?: string;
    id_rol?: number;
    estado?: EstadoLaboral;
    page?: number;
    pageSize?: number;
  }): Observable<Personal[]> {
    let params = new HttpParams();
    
    if (options?.page) params = params.set('page', options.page.toString());
    if (options?.pageSize) params = params.set('page_size', options.pageSize.toString());
    if (options?.search) params = params.set('buscar', options.search);
    if (options?.id_rol) params = params.set('id_rol', options.id_rol.toString());
    if (options?.estado) params = params.set('estado', options.estado);
    
    return this.http.get<PersonalListResponse>(`${this.baseUrl}/`, { params })
      .pipe(
        map(response => this.transformListResponse(response))
      );
  }

  getPersonalById(id: number): Observable<Personal> {
    return this.http.get<PersonalBackendResponse>(`${this.baseUrl}/${id}`)
      .pipe(
        map(personal => this.transformBackendToFrontend(personal))
      );
  }

  createPersonal(data: FormData): Observable<Personal> {
    return this.http.post<PersonalBackendResponse>(`${this.baseUrl}/`, data)
      .pipe(
        map(personal => this.transformBackendToFrontend(personal))
      );
  }

  updatePersonal(id: number, data: FormData): Observable<Personal> {
    return this.http.put<PersonalBackendResponse>(`${this.baseUrl}/${id}`, data)
      .pipe(
        map(personal => this.transformBackendToFrontend(personal))
      );
  }

  cambiarEstado(id: number, estado: EstadoLaboral): Observable<any> {
    return this.http.patch(`${this.baseUrl}/${id}/estado?estado=${estado}`, {});
  }

  deletePersonal(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }

  // ===== HORARIOS =====
  getHorarios(id_personal: number): Observable<HorarioPersonal[]> {
    return this.http.get<HorarioPersonal[]>(`${this.baseUrl}/${id_personal}/horarios`);
  }

  createHorario(horario: HorarioPersonal): Observable<HorarioPersonal> {
    return this.http.post<HorarioPersonal>(`${this.baseUrl}/horarios`, horario);
  }

  updateHorario(id_horario: number, horario: Partial<HorarioPersonal>): Observable<HorarioPersonal> {
    return this.http.put<HorarioPersonal>(`${this.baseUrl}/horarios/${id_horario}`, horario);
  }

  deleteHorario(id_horario: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/horarios/${id_horario}`);
  }

  // ===== DATOS COMPLETOS =====
  getDatosCompletos(id_personal: number): Observable<DatosCompletosPersonal> {
    return this.http.get<DatosCompletosPersonal>(
      `${environment.apiBaseUrl}/coordinador/personal/${id_personal}/datos-completos`
    );
  }

  // ===== TRANSFORMACIONES =====
  private transformListResponse(response: PersonalListResponse): Personal[] {
    return response.items.map(item => this.transformBackendToFrontend(item));
  }

  private transformBackendToFrontend(backend: PersonalBackendResponse): Personal {
    return {
      id_personal: backend.id_personal,
      nombres: backend.nombres,
      apellido_paterno: backend.apellido_paterno,
      apellido_materno: backend.apellido_materno || null,
      id_rol: backend.id_rol,
      especialidad_principal: backend.especialidad_principal || '',
      telefono_personal: backend.telefono_personal,
      correo_personal: backend.correo_personal,
      fecha_ingreso: backend.fecha_ingreso,
      estado_laboral: backend.estado_laboral,
      total_pacientes: backend.total_pacientes || 0,
      sesiones_semana: backend.sesiones_semana || 0,
      rating: backend.rating || 0,
      fecha_nacimiento: backend.fecha_nacimiento || '',
      grado_academico: backend.grado_academico || '',
      especialidades: backend.especialidades || '',
      rfc: backend.rfc || '',
      ine: backend.ine || '',
      curp: backend.curp || '',
      domicilio_calle: backend.domicilio_calle || '',
      domicilio_colonia: backend.domicilio_colonia || '',
      domicilio_cp: backend.domicilio_cp || '',
      domicilio_municipio: backend.domicilio_municipio || '',
      domicilio_estado: backend.domicilio_estado || '',
      cv_archivo: backend.cv_archivo || null,
      experiencia: backend.experiencia || '',
      horarios: backend.horarios || []
    };
  }
}
