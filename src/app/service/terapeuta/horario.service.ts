import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { EventoHorario } from '../../interfaces/terapeuta/evento-horario.interface';

@Injectable({ providedIn: 'root' })
export class HorarioService {

  private base = `${environment.apiBaseUrl}/terapeuta`;

  constructor(private http: HttpClient) {}

  getHorarioSemanal(): Observable<EventoHorario[]> {
    return this.http.get<EventoHorario[]>(`${this.base}/horario`);
  }
}
