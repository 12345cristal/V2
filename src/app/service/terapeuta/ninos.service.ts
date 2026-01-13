import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Nino } from '../../interfaces/terapeuta/nino.interface';

@Injectable({ providedIn: 'root' })
export class NinosService {

  private readonly api = `${environment.apiBaseUrl}/terapeuta/ninos`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene todos los niños asignados al terapeuta
   * (basado en terapias_nino.terapeuta_id)
   */
  getMisNinos(): Observable<Nino[]> {
    return this.http.get<Nino[]>(this.api);
  }

  /**
   * Obtiene detalle de un niño (solo si pertenece al terapeuta)
   */
  getNinoById(ninoId: number): Observable<Nino> {
    return this.http.get<Nino>(`${this.api}/${ninoId}`);
  }

}
