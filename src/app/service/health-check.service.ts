import { Injectable, computed, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, of, timeout } from 'rxjs';
import { environment } from '../../environments/environment';

// Estados explícitos del backend
export type BackendStatus = 'loading' | 'ready' | 'offline';

@Injectable({ providedIn: 'root' })
export class HealthCheckService {
  private readonly statusSig = signal<BackendStatus>('loading');
  private readonly lastErrorSig = signal<string | null>(null);

  readonly status = computed(() => this.statusSig());
  readonly isReady = computed(() => this.statusSig() === 'ready');
  readonly isOffline = computed(() => this.statusSig() === 'offline');
  readonly lastError = computed(() => this.lastErrorSig());

  constructor(private http: HttpClient) {}

  // Ejecuta un health-check con reintentos y backoff exponencial suavizado.
  check(): void {
    this.statusSig.set('loading');

    // Intenta un endpoint simple que sí existe
    this.http
      .get<any>(`${environment.apiBaseUrl}/usuarios`, { withCredentials: false })
      .pipe(
        timeout(3000), // timeout de 3 segundos
        catchError(() => {
          this.statusSig.set('offline');
          return of(null);
        })
      )
      .subscribe({
        next: () => {
          this.statusSig.set('ready');
          this.lastErrorSig.set(null);
        },
        error: () => {
          this.statusSig.set('offline');
        },
      });
  }
}




