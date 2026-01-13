// src/app/service/fichas-emergencia.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface FichaEmergencia {
  id?: number;
  nino_id: number;
  tipo_sangre?: string;
  alergias?: string;
  condiciones_medicas?: string;
  medicamentos_actuales?: string;
  diagnostico_principal?: string;
  diagnostico_detallado?: string;
  
  // Contacto principal
  contacto_principal_nombre: string;
  contacto_principal_relacion?: string;
  contacto_principal_telefono: string;
  contacto_principal_telefono_alt?: string;
  
  // Contacto secundario
  contacto_secundario_nombre?: string;
  contacto_secundario_relacion?: string;
  contacto_secundario_telefono?: string;
  
  // Información médica
  seguro_medico?: string;
  numero_seguro?: string;
  hospital_preferido?: string;
  medico_tratante?: string;
  telefono_medico?: string;
  
  // Instrucciones
  instrucciones_emergencia?: string;
  restricciones_alimenticias?: string;
  
  // Comportamiento
  crisis_comunes?: string;
  como_calmar?: string;
  trigger_points?: string;
  
  // Control
  activa?: boolean;
  fecha_creacion?: string;
  fecha_actualizacion?: string;
  
  // Datos enriquecidos del niño
  nino_nombre_completo?: string;
  nino_foto_url?: string;
  nino_edad?: number;
  nino_estado?: string;
}

export interface FichaEmergenciaImprimible {
  nino_nombre_completo: string;
  nino_foto_url?: string;
  nino_fecha_nacimiento?: string;
  nino_edad?: number;
  nino_sexo?: string;
  tipo_sangre?: string;
  alergias?: string;
  diagnostico_principal?: string;
  medicamentos_actuales?: string;
  contacto_principal_nombre: string;
  contacto_principal_relacion?: string;
  contacto_principal_telefono: string;
  contacto_principal_telefono_alt?: string;
  contacto_secundario_nombre?: string;
  contacto_secundario_telefono?: string;
  seguro_medico?: string;
  hospital_preferido?: string;
  medico_tratante?: string;
  instrucciones_emergencia?: string;
  crisis_comunes?: string;
  como_calmar?: string;
  fecha_generacion: string;
}

@Injectable({
  providedIn: 'root'
})
export class FichasEmergenciaService {
  private apiUrl = 'http://localhost:8000/api/v1/fichas-emergencia';

  constructor(private http: HttpClient) {}

  listarFichas(): Observable<FichaEmergencia[]> {
    return this.http.get<FichaEmergencia[]>(this.apiUrl);
  }

  obtenerFichaPorNino(ninoId: number): Observable<FichaEmergencia> {
    return this.http.get<FichaEmergencia>(`${this.apiUrl}/nino/${ninoId}`);
  }

  obtenerFicha(fichaId: number): Observable<FichaEmergencia> {
    return this.http.get<FichaEmergencia>(`${this.apiUrl}/${fichaId}`);
  }

  crearFicha(ficha: Partial<FichaEmergencia>): Observable<FichaEmergencia> {
    return this.http.post<FichaEmergencia>(this.apiUrl, ficha);
  }

  actualizarFicha(fichaId: number, datos: Partial<FichaEmergencia>): Observable<FichaEmergencia> {
    return this.http.put<FichaEmergencia>(`${this.apiUrl}/${fichaId}`, datos);
  }

  desactivarFicha(fichaId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${fichaId}`);
  }

  obtenerFichaImprimible(ninoId: number): Observable<FichaEmergenciaImprimible> {
    return this.http.get<FichaEmergenciaImprimible>(`${this.apiUrl}/imprimir/nino/${ninoId}`);
  }
}




