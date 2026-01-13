// src/app/service/health-check.service.ts
import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, tap, throwError } from 'rxjs';
import { environment } from '../../environments/environment';

export interface HealthStatus {
  status: string;
  detail?: string;
}

@Injectable({ providedIn: 'root' })
export class HealthCheckService {
  status = signal<'loading' | 'ok' | 'down'>('loading');
  isReady = signal(false);

  constructor(private http: HttpClient) {}

  check(): Observable<HealthStatus> {
    this.status.set('loading');
    this.isReady.set(false);

    return this.http.get<HealthStatus>(`${environment.apiBaseUrl}/ia/estado`).pipe(
      tap(() => {
        this.status.set('ok');
        this.isReady.set(true);
      }),
      catchError(err => {
        this.status.set('down');
        this.isReady.set(false);
        return throwError(() => err);
      })
    );
  }
}
