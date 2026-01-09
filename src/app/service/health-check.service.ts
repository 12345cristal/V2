import { Injectable, computed, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, of, retry, timer } from 'rxjs';
import { environment } from '../enviroment/environment';

// Estados explícitos del backend
export type BackendStatus = 'loading' | 'ready' | 'offline';

@Injectable({ providedIn: 'root' })
export class HealthCheckService {
  private readonly statusSig = signal<BackendStatus>('loading');
  private readonly lastErrorSig = signal<string | null>(null);
  private checking = false;

  readonly status = computed(() => this.statusSig());
  readonly isReady = computed(() => this.statusSig() === 'ready');
  readonly isOffline = computed(() => this.statusSig() === 'offline');
  readonly lastError = computed(() => this.lastErrorSig());

  constructor(private http: HttpClient) {}

  // Ejecuta un health-check con reintentos y backoff exponencial suavizado.
  check(): void {
    if (this.checking) return;
    this.checking = true;
    this.statusSig.set('loading');

    this.http
      .get<{ estado?: string }>(`${environment.apiBaseUrl}/ia/estado`, { withCredentials: false })
      .pipe(
        retry({
          count: 2,
          delay: (_error, retryIndex) => timer(Math.min(500 * (retryIndex + 1), 4000)),
        }),
        catchError((err) => {
          this.statusSig.set('offline');
          this.lastErrorSig.set(err?.message ?? 'backend offline');
          return of({ estado: 'offline' });
        })
      )
      .subscribe({
        next: (res) => {
          if (res?.estado === 'ok' || res?.estado === 'ready') {
            this.statusSig.set('ready');
            this.lastErrorSig.set(null);
          } else if (this.statusSig() !== 'offline') {
            this.statusSig.set('loading');
          }
        },
        error: () => {
          this.statusSig.set('offline');
        },
        complete: () => {
          this.checking = false;
        },
      });
  }
}
