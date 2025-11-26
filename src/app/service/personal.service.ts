import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Personal, Rol } from '../coordinador/interfaces/personal.interface';

// IMPORTA EL ENVIRONMENT
import { environment } from '../enviroment/environment';

@Injectable({
  providedIn: 'root'
})
export class PersonalService {

  private api = environment.apiUrl;

  private personalUrl = `${this.api}/personal`;
  private rolesUrl = `${this.api}/roles`;

  constructor(private http: HttpClient) {}

  // ===== ROLES =====
  getRoles(): Observable<Rol[]> {
    return this.http.get<Rol[]>(this.rolesUrl);
  }

  // ===== PERSONAL =====
  getPersonal(): Observable<Personal[]> {
    return this.http.get<Personal[]>(this.personalUrl);
  }

  getPersonalById(id: number): Observable<Personal> {
    return this.http.get<Personal>(`${this.personalUrl}/${id}`);
  }

  createPersonal(data: FormData | Personal): Observable<Personal> {
    return this.http.post<Personal>(this.personalUrl, data);
  }

  updatePersonal(id: number, data: FormData | Personal): Observable<Personal> {
    return this.http.put<Personal>(`${this.personalUrl}/${id}`, data);
  }

  deletePersonal(id: number): Observable<void> {
    return this.http.delete<void>(`${this.personalUrl}/${id}`);
  }
}
