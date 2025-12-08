import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; // <- IMPORTAR
import { DashboardCoordinadorService } from '../../service/inicio-coordinador.service';
import { DashboardCoordinador } from '../../interfaces/inicio-coordinador.interface';

@Component({
  selector: 'app-dashboard-coordinador',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule // <- AÑADIR AQUÍ
  ],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio.scss']
})
export class InicioComponent implements OnInit {

  data: DashboardCoordinador | null = null;
  cargando = false;
  error = '';

  indicador1: any = null;
  indicador2: any = null;
  indicador3: any = null;

  topTerapeuta1: any = null;
  topTerapeuta2: any = null;
  topTerapeuta3: any = null;

  nino1: any = null;
  nino2: any = null;
  nino3: any = null;

  constructor(private dashboardService: DashboardCoordinadorService) {}

  ngOnInit(): void {
    this.cargar();
  }

  cargar() {
    this.cargando = true;
    this.error = '';

    this.dashboardService.getDashboard().subscribe({
      next: res => {
        console.log('Dashboard cargado:', res);
        this.data = res;

        // KPIs
        this.indicador1 = res.indicadores[0] ?? null;
        this.indicador2 = res.indicadores[1] ?? null;
        this.indicador3 = res.indicadores[2] ?? null;

        // Top terapeutas
        this.topTerapeuta1 = res.topTerapeutas[0] ?? null;
        this.topTerapeuta2 = res.topTerapeutas[1] ?? null;
        this.topTerapeuta3 = res.topTerapeutas[2] ?? null;

        // Niños en riesgo
        this.nino1 = res.ninosEnRiesgo[0] ?? null;
        this.nino2 = res.ninosEnRiesgo[1] ?? null;
        this.nino3 = res.ninosEnRiesgo[2] ?? null;

        this.cargando = false;
      },
      error: err => {
        console.error('Error al cargar dashboard:', err);
        this.error = 'No se pudo cargar el dashboard. Por favor, intenta de nuevo.';
        this.cargando = false;
      }
    });
  }
}
