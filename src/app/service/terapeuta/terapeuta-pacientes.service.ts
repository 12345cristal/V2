import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { NinoResumenTerapeuta } from '../../interfaces/terapeuta/nino-resumen-terapeuta.interface';

@Injectable({
  providedIn: 'root'
})
export class TerapeutaPacientesService {

  // ⚠️ IMPORTANTE: plural "terapeutas"
  private readonly baseUrl = `${environment.apiBaseUrl}/terapeutas`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene los niños asignados al terapeuta autenticado
   */
  getPacientesAsignados(): Observable<NinoResumenTerapeuta[]> {
    return this.http.get<NinoResumenTerapeuta[]>(
      `${this.baseUrl}/mis-pacientes`
    );
  }
}
