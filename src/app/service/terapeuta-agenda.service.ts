import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { SesionTerapia } from '../interfaces/horario-terapeuta.interface';
import { ReposicionTerapia } from '../interfaces/reposicion-terapia.interface';
import { environment } from 'src/environments/environment';

export interface AccionResultado {
  exito: boolean;
  mensaje: string;
  advertencias?: string[]; // ej: "No se registró bitácora", "Objetivo X incompleto"
}

@Injectable({ providedIn: 'root' })
export class TerapeutaAgendaService {

  private api = `${environment.apiBaseUrl}/terapeutas`;

  constructor(private http: HttpClient) {}

  getSesionesSemana() {
    return this.http.get<SesionTerapia[]>(`${this.api}/horarios/semana`);
  }

  getReposiciones() {
    return this.http.get<ReposicionTerapia[]>(`${this.api}/reposiciones`);
  }

  marcarSesionCompletada(idSesion: number) {
    // el backend decide si falta bitácora, objetivos, etc.
    return this.http.post<AccionResultado>(`${this.api}/sesiones/${idSesion}/completar`, {});
  }

  aprobarReposicion(id: number) {
    return this.http.post<AccionResultado>(`${this.api}/reposiciones/${id}/aprobar`, {});
  }

  rechazarReposicion(id: number) {
    return this.http.post<AccionResultado>(`${this.api}/reposiciones/${id}/rechazar`, {});
  }
}

