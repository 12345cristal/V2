import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { DashboardCoordinadorService } from '../../service/inicio-coordinador.service';
import { DashboardCoordinador } from '../../interfaces/inicio-coordinador.interface';

@Component({
  selector: 'app-dashboard-coordinador',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule
  ],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush  // 🔑 IMPORTANTE: OnPush para evitar change after check
})
export class InicioComponent implements OnInit {

  // Inicializar con valores por defecto, nunca undefined
  data: DashboardCoordinador | null = null;
  cargando = false;
  error = '';

  indicador1: any = { titulo: 'Terapeutas Activos', valor: 0, unidad: 'personas', tendencia: 'flat' };
  indicador2: any = { titulo: 'Citas Esta Semana', valor: 0, unidad: 'citas', tendencia: 'up' };
  indicador3: any = { titulo: 'Niños Activos', valor: 0, unidad: 'niños', tendencia: 'flat' };

  topTerapeuta1: any = null;
  topTerapeuta2: any = null;
  topTerapeuta3: any = null;

  nino1: any = null;
  nino2: any = null;
  nino3: any = null;

  constructor(
    private dashboardService: DashboardCoordinadorService
  ) {}

  ngOnInit(): void {
    console.log('🎯 Componente InicioComponent cargado - ngOnInit');
    this.cargar();
  }

  cargar() {
    console.log('📡 Llamando a getDashboard...');
    this.cargando = true;
    this.error = '';

    this.dashboardService.getDashboard().subscribe({
      next: res => {
        console.log('✅ Dashboard cargado:', res);
        this.data = res;

        // KPIs - Asignar directamente sin dejar undefined
        if (res.indicadores?.length >= 3) {
          this.indicador1 = res.indicadores[0];
          this.indicador2 = res.indicadores[1];
          this.indicador3 = res.indicadores[2];
        }

        // Top terapeutas - Usar coalescing
        this.topTerapeuta1 = res.topTerapeutas?.[0] ?? null;
        this.topTerapeuta2 = res.topTerapeutas?.[1] ?? null;
        this.topTerapeuta3 = res.topTerapeutas?.[2] ?? null;

        // Niños en riesgo
        this.nino1 = res.ninosEnRiesgo?.[0] ?? null;
        this.nino2 = res.ninosEnRiesgo?.[1] ?? null;
        this.nino3 = res.ninosEnRiesgo?.[2] ?? null;

        this.cargando = false;
      },
      error: err => {
        console.error('❌ Error al cargar dashboard:', err);
        this.error = err?.error?.detail || 'No se pudo cargar el dashboard. Verifica tu autenticación.';
        this.cargando = false;
      }
    });
  }
}
