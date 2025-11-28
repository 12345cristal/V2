import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NinoResumenTerapeuta } from '../interfaces/nino-resumen-terapeuta.interface';
import { environment } from '../enviroment/environment';

@Injectable({
  providedIn: 'root'
})
export class TerapeutaPacientesService {

  private apiUrl = `${environment.apiBaseUrl}/citas`;

  constructor(private http: HttpClient) {}

  // Lista de niños vinculados al terapeuta
  getPacientesAsignados() {
    return this.http.get<NinoResumenTerapeuta[]>(`${this.api}/mis-pacientes`);
  }

  // Detalles completos de un niño
  getDetallePaciente(id: number) {
    return this.http.get<NinoResumenTerapeuta>(`${this.api}/paciente/${id}`);
  }

getHistorialBitacora(id: number) {
  return this.http.get<BitacoraEntrada[]>(`${this.api}/paciente/${id}/bitacora`);
}

registrarBitacora(id: number, entrada: FormData) {
  return this.http.post(`${this.api}/paciente/${id}/bitacora`, entrada);
}


}
