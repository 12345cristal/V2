import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { NinoResumenTerapeuta } from '../../interfaces/terapeuta/nino-resumen-terapeuta.interface';

@Injectable({ providedIn: 'root' })
export class TerapeutaPacientesService {

  private readonly api = `${environment.apiBaseUrl}/terapeuta`;

  constructor(private http: HttpClient) {}

  getPacientesAsignados(): Observable<NinoResumenTerapeuta[]> {
    return this.http.get<NinoResumenTerapeuta[]>(
      `${this.api}/mis-pacientes`
    );
  }
}
