// src/app/service/ninos.service.ts

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Nino, EstadoNino } from '../interfaces/nino.interface';
import { environment } from '../environments/environment';

// Interfaz para la respuesta del backend
interface NinoBackendResponse {
  id: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  fecha_nacimiento: string;
  sexo: 'M' | 'F' | 'O';
  curp?: string;
  tutor_id?: number;
  estado: EstadoNino;
  fecha_registro: string;
  direccion?: any;
  diagnostico?: any;
  info_emocional?: any;
  archivos?: any;
  tutor_nombre?: string;
}

interface NinoListResponse {
  total: number;
  page: number;
  page_size: number;
  items: {
    id: number;
    nombre: string;
    apellido_paterno: string;
    apellido_materno?: string;
    fecha_nacimiento: string;
    sexo: 'M' | 'F' | 'O';
    edad: number;
    estado: EstadoNino;
    tutor_nombre?: string;
    diagnostico_principal?: string;
  }[];
}

@Injectable({
  providedIn: 'root'
})
export class NinosService {

  private baseUrl = `${environment.apiBaseUrl}/ninos`;

  constructor(private http: HttpClient) {}

  // ============================================================
  // GET — Lista de niños (con filtros opcionales)
  // ============================================================
  getNinos(options?: { search?: string; estado?: EstadoNino | 'TODOS'; page?: number; pageSize?: number }): Observable<Nino[]> {
    let params = new HttpParams();

    // Paginación
    params = params.set('page', (options?.page || 1).toString());
    params = params.set('page_size', (options?.pageSize || 100).toString());

    // Búsqueda
    if (options?.search) {
      params = params.set('buscar', options.search);
    }

    // Estado
    if (options?.estado && options.estado !== 'TODOS') {
      params = params.set('estado', options.estado);
    }

    return this.http.get<NinoListResponse>(`${this.baseUrl}/`, { params })
      .pipe(
        map(response => this.transformListResponse(response))
      );
  }

  // ============================================================
  // GET — Un niño por ID
  // ============================================================
  getNino(id: number): Observable<Nino> {
    return this.http.get<NinoBackendResponse>(`${this.baseUrl}/${id}`)
      .pipe(
        map(nino => this.transformBackendToFrontend(nino))
      );
  }

  // ============================================================
  // POST — Crear niño
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
    const body = this.transformFrontendToBackend(payload.nino);
    return this.http.post<NinoBackendResponse>(`${this.baseUrl}/`, body)
      .pipe(
        map(nino => this.transformBackendToFrontend(nino))
      );
  }

  // ============================================================
  // PUT — Actualizar niño
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
    const body = this.transformFrontendToBackend(payload.nino);
    return this.http.put<NinoBackendResponse>(`${this.baseUrl}/${id}`, body)
      .pipe(
        map(nino => this.transformBackendToFrontend(nino))
      );
  }

  // ============================================================
  // PATCH — Cambiar estado del niño
  // ============================================================
  cambiarEstado(id: number, estado: EstadoNino): Observable<any> {
    return this.http.patch(`${this.baseUrl}/${id}/estado?estado=${estado}`, {});
  }

  // ============================================================
  // DELETE — Eliminar niño
  // ============================================================
  eliminarNino(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }

  // ============================================================
  // GET — Estadísticas
  // ============================================================
  getEstadisticas(): Observable<any> {
    return this.http.get(`${this.baseUrl}/estadisticas/resumen`);
  }

  // ============================================================
  // TRANSFORMACIONES — Backend <-> Frontend
  // ============================================================
  private transformListResponse(response: NinoListResponse): Nino[] {
    return response.items.map(item => ({
      id: item.id,
      nombre: item.nombre,
      apellidoPaterno: item.apellido_paterno,
      apellidoMaterno: item.apellido_materno || '',
      fechaNacimiento: item.fecha_nacimiento,
      edad: item.edad,
      sexo: item.sexo,
      curp: '',
      direccion: { calle: '', numero: '', colonia: '', municipio: '', codigoPostal: '' },
      diagnostico: {
        diagnosticoPrincipal: item.diagnostico_principal || '',
        fechaDiagnostico: null,
        diagnosticosSecundarios: [],
        especialista: '',
        institucion: ''
      },
      alergias: { medicamentos: '', alimentos: '', ambiental: '' },
      medicamentosActuales: [],
      escolar: { escuela: '', grado: '', maestro: '', horarioClases: '', adaptaciones: '' },
      contactosEmergencia: [],
      infoEmocional: {
        estimulosAnsiedad: '',
        cosasQueCalman: '',
        preferenciasSensoriales: '',
        cosasNoTolera: '',
        palabrasClave: '',
        formaComunicacion: '',
        nivelComprension: 'MEDIO'
      },
      infoCentro: {
        fechaIngreso: '',
        terapias: {
          lenguaje: false,
          conductual: false,
          ocupacional: false,
          sensorial: false,
          psicologia: false
        },
        horariosTerapia: '',
        terapeutaAsignado: item.tutor_nombre || '',
        costoMensual: 0,
        modalidadPago: '',
        estado: item.estado
      }
    }));
  }

  private transformBackendToFrontend(nino: NinoBackendResponse): Nino {
    return {
      id: nino.id,
      nombre: nino.nombre,
      apellidoPaterno: nino.apellido_paterno,
      apellidoMaterno: nino.apellido_materno || '',
      fechaNacimiento: nino.fecha_nacimiento,
      sexo: nino.sexo,
      curp: nino.curp || '',
      direccion: nino.direccion ? {
        calle: nino.direccion.calle || '',
        numero: nino.direccion.numero || '',
        colonia: nino.direccion.colonia || '',
        municipio: nino.direccion.municipio || '',
        codigoPostal: nino.direccion.codigo_postal || ''
      } : { calle: '', numero: '', colonia: '', municipio: '', codigoPostal: '' },
      diagnostico: nino.diagnostico ? {
        diagnosticoPrincipal: nino.diagnostico.diagnostico_principal || '',
        fechaDiagnostico: nino.diagnostico.fecha_diagnostico || null,
        diagnosticosSecundarios: [],
        especialista: nino.diagnostico.especialista || '',
        institucion: nino.diagnostico.institucion || ''
      } : {
        diagnosticoPrincipal: '',
        fechaDiagnostico: null,
        diagnosticosSecundarios: [],
        especialista: '',
        institucion: ''
      },
      alergias: { medicamentos: '', alimentos: '', ambiental: '' },
      medicamentosActuales: [],
      escolar: { escuela: '', grado: '', maestro: '', horarioClases: '', adaptaciones: '' },
      contactosEmergencia: [],
      infoEmocional: nino.info_emocional ? {
        estimulosAnsiedad: nino.info_emocional.estimulos || '',
        cosasQueCalman: nino.info_emocional.calmantes || '',
        preferenciasSensoriales: nino.info_emocional.preferencias || '',
        cosasNoTolera: nino.info_emocional.no_tolera || '',
        palabrasClave: nino.info_emocional.palabras_clave || '',
        formaComunicacion: nino.info_emocional.forma_comunicacion || '',
        nivelComprension: nino.info_emocional.nivel_comprension || 'MEDIO'
      } : {
        estimulosAnsiedad: '',
        cosasQueCalman: '',
        preferenciasSensoriales: '',
        cosasNoTolera: '',
        palabrasClave: '',
        formaComunicacion: '',
        nivelComprension: 'MEDIO'
      },
      infoCentro: {
        fechaIngreso: nino.fecha_registro,
        terapias: {
          lenguaje: false,
          conductual: false,
          ocupacional: false,
          sensorial: false,
          psicologia: false
        },
        horariosTerapia: '',
        terapeutaAsignado: nino.tutor_nombre || '',
        costoMensual: 0,
        modalidadPago: '',
        estado: nino.estado
      }
    };
  }

  private transformFrontendToBackend(nino: Nino): any {
    return {
      nombre: nino.nombre,
      apellido_paterno: nino.apellidoPaterno,
      apellido_materno: nino.apellidoMaterno,
      fecha_nacimiento: nino.fechaNacimiento,
      sexo: nino.sexo,
      curp: nino.curp || null,
      tutor_id: null,
      estado: nino.infoCentro.estado,
      direccion: nino.direccion ? {
        calle: nino.direccion.calle,
        numero: nino.direccion.numero,
        colonia: nino.direccion.colonia,
        municipio: nino.direccion.municipio,
        codigo_postal: nino.direccion.codigoPostal
      } : null,
      diagnostico: nino.diagnostico ? {
        diagnostico_principal: nino.diagnostico.diagnosticoPrincipal,
        diagnostico_resumen: nino.diagnostico.diagnosticoPrincipal,
        fecha_diagnostico: nino.diagnostico.fechaDiagnostico,
        especialista: nino.diagnostico.especialista,
        institucion: nino.diagnostico.institucion
      } : null,
      info_emocional: {
        estimulos: nino.infoEmocional.estimulosAnsiedad,
        calmantes: nino.infoEmocional.cosasQueCalman,
        preferencias: nino.infoEmocional.preferenciasSensoriales,
        no_tolera: nino.infoEmocional.cosasNoTolera,
        palabras_clave: nino.infoEmocional.palabrasClave,
        forma_comunicacion: nino.infoEmocional.formaComunicacion,
        nivel_comprension: nino.infoEmocional.nivelComprension
      }
    };
  }
}
