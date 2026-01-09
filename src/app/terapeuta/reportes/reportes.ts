import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { TerapeutaService, ReporteDTO } from '../../service/terapeuta.service';

interface Reporte {
  id_reporte: number;
  id_nino: number;
  nombre_nino: string;
  cuatrimestre: string;
  tipo_reporte: string;
  estado: 'pendiente' | 'subido' | 'aprobado';
  fecha_subida?: Date;
  archivo_url?: string;
  observaciones?: string;
}

@Component({
  selector: 'app-reportes-terapeuta',
  standalone: true,
  imports: [CommonModule, FormsModule, MatIconModule],
  template: `
    <div class="reportes-container">
      <header class="page-header">
        <div class="header-content">
          <button class="btn-back" (click)="volver()">
            <mat-icon>arrow_back</mat-icon>
          </button>
          <div class="title-section">
            <h1>Reportes Cuatrimestrales</h1>
            <p class="subtitle">Gestiona los reportes clínicos de tus pacientes</p>
          </div>
        </div>
        
        <button class="btn-nuevo" (click)="abrirModalSubida()">
          <mat-icon>add</mat-icon>
          Subir reporte
        </button>
      </header>

      <!-- Filtros -->
      <section class="filtros-section">
        <div class="filtro-item">
          <label><mat-icon>filter_list</mat-icon> Estado</label>
          <select [(ngModel)]="estadoFiltro" (change)="filtrar()">
            <option value="todos">Todos</option>
            <option value="pendiente">Pendientes</option>
            <option value="subido">Subidos</option>
            <option value="aprobado">Aprobados</option>
          </select>
        </div>

        <div class="filtro-item">
          <label><mat-icon>calendar_today</mat-icon> Cuatrimestre</label>
          <select [(ngModel)]="cuatrimestreFiltro" (change)="filtrar()">
            <option value="todos">Todos</option>
            <option value="1-2026">Cuatrimestre 1 - 2026</option>
            <option value="2-2026">Cuatrimestre 2 - 2026</option>
            <option value="3-2026">Cuatrimestre 3 - 2026</option>
          </select>
        </div>
      </section>

      <!-- Alertas -->
      @if (reportesPendientes() > 0) {
        <div class="alerta-pendientes">
          <mat-icon>warning</mat-icon>
          <span>Tienes {{ reportesPendientes() }} reporte(s) pendiente(s) de entregar</span>
          <button (click)="filtrarPendientes()">Ver pendientes</button>
        </div>
      }

      <!-- Grid de reportes -->
      <section class="reportes-grid">
        @for (reporte of reportesFiltrados(); track reporte.id_reporte) {
          <article class="reporte-card" [class]="'estado-' + reporte.estado">
            <div class="reporte-header">
              <h3>{{ reporte.nombre_nino }}</h3>
              <span class="estado-badge" [class]="'badge-' + reporte.estado">
                {{ getEstadoTexto(reporte.estado) }}
              </span>
            </div>

            <div class="reporte-info">
              <div class="info-item">
                <mat-icon>calendar_today</mat-icon>
                <span>{{ reporte.cuatrimestre }}</span>
              </div>
              <div class="info-item">
                <mat-icon>description</mat-icon>
                <span>{{ reporte.tipo_reporte }}</span>
              </div>
              @if (reporte.fecha_subida) {
                <div class="info-item">
                  <mat-icon>upload</mat-icon>
                  <span>{{ reporte.fecha_subida | date: 'dd/MM/yyyy' }}</span>
                </div>
              }
            </div>

            <div class="reporte-acciones">
              @if (reporte.estado === 'pendiente') {
                <button class="btn-subir" (click)="subirReporte(reporte)">
                  <mat-icon>cloud_upload</mat-icon>
                  Subir
                </button>
              } @else {
                <button class="btn-ver" (click)="verReporte(reporte)">
                  <mat-icon>visibility</mat-icon>
                  Ver
                </button>
                @if (reporte.estado === 'subido') {
                  <button class="btn-editar" (click)="editarReporte(reporte)">
                    <mat-icon>edit</mat-icon>
                    Editar
                  </button>
                }
              }
            </div>
          </article>
        }
      </section>
    </div>
  `,
  styles: [`
    .reportes-container {
      padding: 24px;
      max-width: 1400px;
      margin: 0 auto;
      background: #f9fafb;
      min-height: 100vh;
    }

    .page-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding: 20px;
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .header-content {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .btn-back {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: none;
      background: #e5e7eb;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;
    }

    .btn-back:hover {
      background: #d1d5db;
      transform: scale(1.05);
    }

    .title-section h1 {
      font-size: 1.75rem;
      font-weight: 700;
      color: #1f2937;
      margin: 0 0 4px 0;
    }

    .title-section .subtitle {
      font-size: 0.95rem;
      color: #6b7280;
      margin: 0;
    }

    .btn-nuevo {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 20px;
      background: #4a90e2;
      color: white;
      border: none;
      border-radius: 10px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .btn-nuevo:hover {
      background: #357abd;
      transform: translateY(-2px);
    }

    .filtros-section {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
      padding: 20px;
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .filtro-item {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .filtro-item label {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.875rem;
      font-weight: 600;
      color: #1f2937;
    }

    .filtro-item select {
      padding: 10px 14px;
      border: 2px solid #e5e7eb;
      border-radius: 8px;
      font-size: 0.9rem;
    }

    .alerta-pendientes {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px 20px;
      background: #fff9e6;
      border: 2px solid #ffd54f;
      border-radius: 12px;
      margin-bottom: 24px;
    }

    .alerta-pendientes mat-icon {
      color: #f57f17;
      font-size: 24px;
    }

    .alerta-pendientes span {
      flex: 1;
      font-weight: 600;
      color: #f57f17;
    }

    .alerta-pendientes button {
      padding: 8px 16px;
      background: #f57f17;
      color: white;
      border: none;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
    }

    .reportes-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
    }

    .reporte-card {
      background: white;
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
      border: 2px solid #e5e7eb;
      transition: all 0.3s ease;
    }

    .reporte-card.estado-pendiente {
      border-color: #fbbf24;
      background: #fffbeb;
    }

    .reporte-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }

    .reporte-header {
      display: flex;
      justify-content: space-between;
      align-items: start;
      margin-bottom: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid #e5e7eb;
    }

    .reporte-header h3 {
      font-size: 1.1rem;
      font-weight: 700;
      color: #1f2937;
      margin: 0;
    }

    .estado-badge {
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
    }

    .badge-pendiente {
      background: #fff3cd;
      color: #856404;
    }

    .badge-subido {
      background: #d1ecf1;
      color: #0c5460;
    }

    .badge-aprobado {
      background: #d4edda;
      color: #155724;
    }

    .reporte-info {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 16px;
    }

    .info-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.875rem;
      color: #4b5563;
    }

    .info-item mat-icon {
      font-size: 18px;
      color: #4a90e2;
    }

    .reporte-acciones {
      display: flex;
      gap: 8px;
    }

    .reporte-acciones button {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 10px;
      border: none;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.875rem;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .btn-subir {
      background: #4a90e2;
      color: white;
    }

    .btn-subir:hover {
      background: #357abd;
      transform: scale(1.05);
    }

    .btn-ver {
      background: #6b7280;
      color: white;
    }

    .btn-ver:hover {
      background: #4b5563;
    }

    .btn-editar {
      background: #fbbf24;
      color: #78350f;
    }

    .btn-editar:hover {
      background: #f59e0b;
    }
  `]
})
export class ReportesTerapeutaComponent implements OnInit {
  
  reportes = signal<Reporte[]>([]);
  reportesFiltrados = signal<Reporte[]>([]);
  
  estadoFiltro = 'todos';
  cuatrimestreFiltro = 'todos';

  constructor(
    private router: Router,
    private terapeutaService: TerapeutaService
  ) {}

  ngOnInit(): void {
    this.cargarReportes();
  }

  cargarReportes(): void {
    this.terapeutaService.obtenerReportes().subscribe({
      next: (reportes) => {
        this.reportes.set(reportes);
        this.filtrar();
      },
      error: (error) => {
        console.error('Error al cargar reportes:', error);
      }
    });
  }

  filtrar(): void {
    let reportes = this.reportes();

    if (this.estadoFiltro !== 'todos') {
      reportes = reportes.filter(r => r.estado === this.estadoFiltro);
    }

    if (this.cuatrimestreFiltro !== 'todos') {
      reportes = reportes.filter(r => r.cuatrimestre === this.cuatrimestreFiltro);
    }

    this.reportesFiltrados.set(reportes);
  }

  reportesPendientes(): number {
    return this.reportes().filter(r => r.estado === 'pendiente').length;
  }

  filtrarPendientes(): void {
    this.estadoFiltro = 'pendiente';
    this.filtrar();
  }

  abrirModalSubida(): void {
    console.log('Abrir modal de subida');
  }

  subirReporte(reporte: Reporte): void {
    console.log('Subir reporte:', reporte);
  }

  verReporte(reporte: Reporte): void {
    console.log('Ver reporte:', reporte);
  }

  editarReporte(reporte: Reporte): void {
    console.log('Editar reporte:', reporte);
  }

  getEstadoTexto(estado: string): string {
    const textos: any = {
      'pendiente': 'Pendiente',
      'subido': 'Subido',
      'aprobado': 'Aprobado'
    };
    return textos[estado] || 'Desconocido';
  }

  volver(): void {
    this.router.navigate(['/terapeuta/inicio']);
  }
}
