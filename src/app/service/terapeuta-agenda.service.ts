import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { SesionTerapia } from '../interfaces/horario-terapeuta.interface';
import { ReposicionTerapia } from '../interfaces/reposicion-terapia.interface';
import { environment } from '../enviroment/environment';
@Injectable({
  providedIn: 'root'
})
export class TerapeutaAgendaService {

  private apiUrl = `${environment.apiBaseUrl}/citas`;

  constructor(private http: HttpClient) {}

  // Horarios de la semana actual
  getSesionesSemana() {
    return this.http.get<SesionTerapia[]>(`${this.api}/horarios/semana`);
  }

  // Todas las reposiciones vinculadas al terapeuta
  getReposiciones() {
    return this.http.get<ReposicionTerapia[]>(`${this.api}/reposiciones`);
  }

  aprobarReposicion(id: number) {
    return this.http.post(`${this.api}/reposiciones/${id}/aprobar`, {});
  }

  rechazarReposicion(id: number) {
    return this.http.post(`${this.api}/reposiciones/${id}/rechazar`, {});
  }
}
