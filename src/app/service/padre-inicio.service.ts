import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DashboardPadre } from '../interfaces/inicio_padre.interface';
import { Hijo } from '../interfaces/hijo.interface';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PadreDashboardService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiBaseUrl;

  getHijos(): Observable<Hijo[]> {
    return this.http.get<Hijo[]>(`${this.apiUrl}/padre/hijos`);
  }

  getDashboard(hijoId: number): Observable<DashboardPadre> {
    return this.http.get<DashboardPadre>(`${this.apiUrl}/padre/dashboard/${hijoId}`);
  }
}




