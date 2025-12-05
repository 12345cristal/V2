import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../enviroment/environment';
import { Observable } from 'rxjs';
import { DashboardCoordinador } from '../interfaces/inicio-coordinador.interface';

@Injectable({ providedIn: 'root' })
export class DashboardCoordinadorService {
  private base = `${environment.apiBaseUrl}/coordinador/dashboard`;

  constructor(private http: HttpClient) {}

  getDashboard(): Observable<DashboardCoordinador> {
    return this.http.get<DashboardCoordinador>(this.base);
  }
}
