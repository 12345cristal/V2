// import { Component, OnInit, ChangeDetectionStrategy, effect, inject } from '@angular/core';
// import { ChangeDetectorRef } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { RouterModule } from '@angular/router';
// import { DashboardCoordinadorService } from '../../service/inicio-coordinador.service';
// import { DashboardCoordinador } from '../../interfaces/inicio-coordinador.interface';
// import { HealthCheckService } from '../../service/health-check.service';

// @Component({
//   selector: 'app-dashboard-coordinador',
//   standalone: true,
//   imports: [
//     CommonModule,
//     RouterModule
//   ],
//   templateUrl: './inicio.html',
//   styleUrls: ['./inicio.scss'],
//   changeDetection: ChangeDetectionStrategy.OnPush  // 🔑 IMPORTANTE: OnPush para evitar change after check
// })
// export class InicioComponent implements OnInit {

//   // Inicializar con valores por defecto, nunca undefined
//   data: DashboardCoordinador | null = null;
//   cargando = false;
//   error = '';

//   indicador1: any = { titulo: 'Terapeutas Activos', valor: 0, unidad: 'personas', tendencia: 'flat' };
//   indicador2: any = { titulo: 'Citas Esta Semana', valor: 0, unidad: 'citas', tendencia: 'up' };
//   indicador3: any = { titulo: 'Niños Activos', valor: 0, unidad: 'niños', tendencia: 'flat' };

//   topTerapeuta1: any = null;
//   topTerapeuta2: any = null;
//   topTerapeuta3: any = null;

//   nino1: any = null;
//   nino2: any = null;
//   nino3: any = null;

//   private dashboardService = inject(DashboardCoordinadorService);
//   private health = inject(HealthCheckService);
//   private cdr = inject(ChangeDetectorRef);
  
//   readonly backendReady = this.health.isReady;
//   readonly backendStatus = this.health.status;

//   constructor() {
//     // Effect: cargar dashboard solo cuando el backend esté ready
//     effect(() => {
//       if (this.backendReady() && !this.data && !this.cargando) {
//         console.log('🎯 Backend ready, cargando dashboard...');
//         this.cargar();
//       }
//     });
//   }

//   ngOnInit(): void {
//     console.log('🎯 Componente InicioComponent cargado - ngOnInit');
//     // Verificar estado del backend primero
//     this.health.check();
//   }

//   reintentarBackend(): void {
//     this.health.check();
//   }

//   cargar() {
//     console.log('📡 Llamando a getDashboard...');
//     this.cargando = true;
//     this.error = '';

//     this.dashboardService.getDashboard().subscribe({
//       next: res => {
//         console.log('✅ Dashboard cargado:', res);
//         this.data = res;

//         // KPIs - Asignar directamente sin dejar undefined
//         if (res.indicadores?.length >= 3) {
//           this.indicador1 = res.indicadores[0];
//           this.indicador2 = res.indicadores[1];
//           this.indicador3 = res.indicadores[2];
//         }

//         // Top terapeutas - Usar coalescing
//         this.topTerapeuta1 = res.topTerapeutas?.[0] ?? null;
//         this.topTerapeuta2 = res.topTerapeutas?.[1] ?? null;
//         this.topTerapeuta3 = res.topTerapeutas?.[2] ?? null;

//         // Niños en riesgo
//         this.nino1 = res.ninosEnRiesgo?.[0] ?? null;
//         this.nino2 = res.ninosEnRiesgo?.[1] ?? null;
//         this.nino3 = res.ninosEnRiesgo?.[2] ?? null;

//         this.cargando = false;
//         this.cdr.markForCheck();
//       },
//       error: err => {
//         console.error('❌ Error al cargar dashboard:', err);
//         this.error = err?.error?.detail || 'No se pudo cargar el dashboard. Verifica tu autenticación.';
//         this.cargando = false;
//         this.cdr.markForCheck();
//       }
//     });
//   }
// }



// src/app/coordinador/inicio/inicio.ts
import { Component, OnInit, ChangeDetectionStrategy, effect, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';

import { DashboardCoordinadorService } from '../../service/inicio-coordinador.service';
import { HealthCheckService } from '../../service/health-check.service';

@Component({
  selector: 'app-dashboard-coordinador',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class InicioComponent implements OnInit {

  private dashboard = inject(DashboardCoordinadorService);
  private health = inject(HealthCheckService);
  private cdr = inject(ChangeDetectorRef);

  readonly backendReady = this.health.isReady;
  readonly backendStatus = this.health.status;

  data: any = null;
  cargando = false;
  error = '';

  constructor() {
    effect(() => {
      if (this.backendReady() && !this.data && !this.cargando) {
        this.cargar();
      }
    });
  }

  ngOnInit(): void {
    this.health.check().subscribe();
  }

  reintentarBackend(): void {
    this.health.check().subscribe();
  }

  cargar(): void {
    this.cargando = true;
    this.dashboard.getDashboard().subscribe({
      next: res => {
        this.data = res;
        this.cargando = false;
        this.cdr.markForCheck();
      },
      error: () => {
        this.error = 'Error cargando dashboard';
        this.cargando = false;
        this.cdr.markForCheck();
      }
    });
  }
}
