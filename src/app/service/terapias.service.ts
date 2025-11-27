import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../enviroment/environment';
import { Terapia, AsignacionTerapia } from '../coordinador/interfaces/terapia.interfaz';

@Injectable({
  providedIn: 'root'
})
export class TherapyService {

  private api = `${environment.apiBaseUrl}/terapias`;

  constructor(private http: HttpClient) {}

  getTerapias() {
    return this.http.get<Terapia[]>(`${this.api}`);
  }

  getPersonalDisponible() {
    return this.http.get(`${environment.apiBaseUrl}/personal/sin-terapia`);
  }

  getPersonalAsignado() {
    return this.http.get(`${this.api}/personal-asignado`);
  }

  crearTerapia(data: Terapia) {
    return this.http.post(`${this.api}`, data);
  }

  actualizarTerapia(id: number, data: Terapia) {
    return this.http.put(`${this.api}/${id}`, data);
  }

  cambiarEstado(id: number) {
    return this.http.patch(`${this.api}/${id}/estado`, {});
  }

  asignarPersonal(data: AsignacionTerapia) {
    return this.http.post(`${this.api}/asignar`, data);
  }
}
