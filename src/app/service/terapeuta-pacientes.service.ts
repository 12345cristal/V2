import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { NinoResumenTerapeuta } from '../interfaces/nino-resumen-terapeuta.interface';
import { BitacoraEntrada, BitacoraResultado } from '../interfaces/bitacora.interface';
import { environment } from '../enviroment/environment';

@Injectable({ providedIn: 'root' })
export class TerapeutaPacientesService {

  private api = `${environment.apiBaseUrl}/terapeutas`;

  constructor(private http: HttpClient) {}

  getPacientesAsignados() {
    return this.http.get<NinoResumenTerapeuta[]>(`${this.api}/mis-pacientes`);
  }

  getDetallePaciente(id: number) {
    return this.http.get<NinoResumenTerapeuta>(`${this.api}/pacientes/${id}`);
  }

  getHistorialBitacora(id: number) {
    return this.http.get<BitacoraEntrada[]>(`${this.api}/pacientes/${id}/bitacora`);
  }

  registrarBitacora(id: number, payload: FormData) {
    return this.http.post<BitacoraResultado>(`${this.api}/pacientes/${id}/bitacora`, payload);
  }
}
