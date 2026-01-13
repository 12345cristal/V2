import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable, of, forkJoin, from, catchError, map, timeout } from 'rxjs';
import { environment } from '../../environments/environment';

export type HealthState = 'up' | 'down';

export interface HealthResult {
  api: HealthState;
  files: HealthState;
  ws: HealthState;
}
@Injectable({ providedIn: 'root' })
export class HealthCheckService {
  constructor(private http: HttpClient) {}

  checkApi(timeoutMs = 3000): Observable<'up' | 'down'> {
    return this.http
      .get(`${environment.apiBaseUrl}/ia/estado`, { observe: 'response' })
      .pipe(
        timeout(timeoutMs),
        map(res => (res.status >= 200 && res.status < 300 ? 'up' : 'down')),
        catchError(() => of<'up' | 'down'>('down'))
      );
  }
}
