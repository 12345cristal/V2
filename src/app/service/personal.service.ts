import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Personal, PersonalCreateDto, PersonalUpdateDto } from '../coordinador/personal/personal.interface';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PersonalService {

  private api = 'http://localhost:8000'; // AJUSTA TU HOST

  constructor(private http: HttpClient) {}

  getPersonal(): Observable<Personal[]> {
    return this.http.get<Personal[]>(`${this.api}/personal`);
  }

  getRoles(): Observable<any[]> {
    return this.http.get<any[]>(`${this.api}/roles`);
  }

  getPersonalById(id: number): Observable<Personal> {
    return this.http.get<Personal>(`${this.api}/personal/${id}`);
  }

  createPersonal(dto: PersonalCreateDto): Observable<Personal> {
    return this.http.post<Personal>(`${this.api}/personal`, dto);
  }

  updatePersonal(id: number, dto: PersonalUpdateDto): Observable<Personal> {
    return this.http.put<Personal>(`${this.api}/personal/${id}`, dto);
  }

  cambiarEstado(id: number, activo: boolean): Observable<any> {
    return this.http.patch(`${this.api}/personal/${id}/estado`, { activo });
  }
}
