import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';

@Injectable({ providedIn: 'root' })
export class HorarioService {

  private readonly api = `${environment.apiBaseUrl}/terapeuta/horario`;

  constructor(private http: HttpClient) {}

  /**
   * Horario semanal del terapeuta
   * (personal_horario + citas)
   */
  getHorarioSemanal(): Observable<any[]> {
    return this.http.get<any[]>(this.api);
  }

}
