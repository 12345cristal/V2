import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Recurso {
  id: string;
  titulo: string;
  tipo: 'pdf' | 'video' | 'enlace';
  descripcion: string;
  asignadoPor: string;
  objetivoTerapeutico: string;
  visto: boolean;
  url?: string;
  fechaAsignacion: Date;
}

@Component({
  selector: 'app-recursos',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="recursos-container">
      <h1>📚 Recursos Recomendados</h1>

      <div class="filtros">
        <div class="filtro-group">
          <label>Filtrar por tipo:</label>
          <select [(ngModel)]="filtroTipo" (change)="aplicarFiltros()">
            <option value="">Todos</option>
            <option value="pdf">PDFs</option>
            <option value="video">Videos</option>
            <option value="enlace">Enlaces</option>
          </select>
        </div>

        <div class="filtro-group">
          <label>Filtrar por estado:</label>
          <select [(ngModel)]="filtroEstado" (change)="aplicarFiltros()">
            <option value="">Todos</option>
            <option value="visto">Vistos</option>
            <option value="no-visto">No vistos</option>
          </select>
        </div>
      </div>

      <div class="recursos-list">
        <div *ngFor="let recurso of recursosFiltrados" 
             class="recurso-card"
             [class.visto]="recurso.visto">
          <div class="recurso-header">
            <div class="recurso-icon">
              <span *ngIf="recurso.tipo === 'pdf'">📄</span>
              <span *ngIf="recurso.tipo === 'video'">🎥</span>
              <span *ngIf="recurso.tipo === 'enlace'">🔗</span>
            </div>
            <div class="recurso-info">
              <h3>{{ recurso.titulo }}</h3>
              <p class="tipo">{{ recurso.tipo | uppercase }}</p>
            </div>
            <div class="recurso-estado">
              <span class="badge" [class.visto]="recurso.visto">
                {{ recurso.visto ? '👀 Visto' : '👁️ No visto' }}
              </span>
            </div>
          </div>

          <p class="descripcion">{{ recurso.descripcion }}</p>

          <div class="metadata">
            <p><strong>Objetivo:</strong> {{ recurso.objetivoTerapeutico }}</p>
            <p><strong>Asignado por:</strong> {{ recurso.asignadoPor }}</p>
            <p><strong>Fecha:</strong> {{ recurso.fechaAsignacion | date: 'shortDate' }}</p>
          </div>

          <div class="acciones">
            <button *ngIf="recurso.url" (click)="abrirRecurso(recurso)" class="btn-ver">
              {{ recurso.tipo === 'pdf' ? '📥 Descargar' : '▶️ Ver' }}
            </button>
            <button (click)="marcarVisto(recurso)" 
                    [class.active]="recurso.visto"
                    class="btn-visto">
              {{ recurso.visto ? '✓ Marcado como visto' : 'Marcar como visto' }}
            </button>
          </div>
        </div>

        <div *ngIf="recursosFiltrados.length === 0" class="sin-recursos">
          <p>No hay recursos con los filtros seleccionados</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .recursos-container {
      padding: 2rem;
      max-width: 900px;
      margin: 0 auto;
    }

    h1 {
      color: #2c3e50;
      margin-bottom: 2rem;
    }

    .filtros {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .filtro-group {
      display: flex;
      flex-direction: column;

      label {
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
      }

      select {
        padding: 0.75rem;
        border: 2px solid #ecf0f1;
        border-radius: 8px;
        background: white;
        color: #2c3e50;
        cursor: pointer;

        &:focus {
          outline: none;
          border-color: #3498db;
        }
      }
    }

    .recursos-list {
      display: grid;
      gap: 1.5rem;
    }

    .recurso-card {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      transition: all 0.3s;
      border-left: 4px solid #3498db;

      &:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
      }

      &.visto {
        opacity: 0.8;
        background: #f8f9fa;
      }
    }

    .recurso-header {
      display: flex;
      gap: 1rem;
      margin-bottom: 1rem;
      align-items: flex-start;
    }

    .recurso-icon {
      font-size: 2rem;
      min-width: 50px;
      text-align: center;
    }

    .recurso-info {
      flex: 1;

      h3 {
        margin: 0 0 0.25rem 0;
        color: #2c3e50;
      }

      .tipo {
        margin: 0;
        color: #7f8c8d;
        font-size: 0.85rem;
        font-weight: 600;
      }
    }

    .recurso-estado {
      flex-shrink: 0;
    }

    .badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      background: #fff5e5;
      color: #d68910;

      &.visto {
        background: #e5ffe5;
        color: #27ae60;
      }
    }

    .descripcion {
      color: #555;
      margin: 1rem 0;
      line-height: 1.5;
    }

    .metadata {
      background: #f8f9fa;
      padding: 1rem;
      border-radius: 8px;
      margin: 1rem 0;

      p {
        margin: 0.5rem 0;
        font-size: 0.95rem;
        color: #666;

        strong {
          color: #2c3e50;
        }
      }
    }

    .acciones {
      display: flex;
      gap: 1rem;
      margin-top: 1rem;
    }

    .btn-ver, .btn-visto {
      padding: 0.75rem 1.5rem;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.3s;
      flex: 1;

      &:hover {
        transform: translateY(-2px);
      }
    }

    .btn-ver {
      background: #3498db;
      color: white;

      &:hover {
        background: #2980b9;
      }
    }

    .btn-visto {
      background: #ecf0f1;
      color: #7f8c8d;

      &:hover {
        background: #d5dbdb;
      }

      &.active {
        background: #2ecc71;
        color: white;
      }
    }

    .sin-recursos {
      text-align: center;
      padding: 2rem;
      color: #95a5a6;

      p {
        margin: 0;
      }
    }

    @media (max-width: 768px) {
      .filtros {
        grid-template-columns: 1fr;
      }

      .recurso-header {
        flex-wrap: wrap;
      }

      .acciones {
        flex-direction: column;
      }
    }
  `]
})
export class RecursosComponent implements OnInit {
  recursos: Recurso[] = [];
  recursosFiltrados: Recurso[] = [];
  filtroTipo: string = '';
  filtroEstado: string = '';

  ngOnInit() {
    this.cargarRecursos();
    this.aplicarFiltros();
  }

  private cargarRecursos() {
    this.recursos = [
      {
        id: '1',
        titulo: 'Estrategias de comunicación efectiva',
        tipo: 'pdf',
        descripcion: 'Guía completa con técnicas para mejorar la comunicación con niños en el espectro autista',
        asignadoPor: 'Dra. María García',
        objetivoTerapeutico: 'Habilidades comunicacionales',
        visto: true,
        url: 'resources/comunicacion.pdf',
        fechaAsignacion: new Date('2025-12-15'),
      },
      {
        id: '2',
        titulo: 'Ejercicios de respiración para ansiedad',
        tipo: 'video',
        descripcion: 'Video tutorial mostrando técnicas de respiración paso a paso',
        asignadoPor: 'Dra. Carolina López',
        objetivoTerapeutico: 'Control emocional',
        visto: false,
        url: 'https://youtube.com/...',
        fechaAsignacion: new Date('2026-01-08'),
      },
      {
        id: '3',
        titulo: 'Socialización en grupos pequeños',
        tipo: 'enlace',
        descripcion: 'Blog con actividades y dinámicas para mejorar interacción social',
        asignadoPor: 'Dra. María García',
        objetivoTerapeutico: 'Socialización',
        visto: false,
        url: 'https://example.com/socializacion',
        fechaAsignacion: new Date('2026-01-05'),
      },
    ];
  }

  aplicarFiltros() {
    this.recursosFiltrados = this.recursos.filter(r => {
      const cumpleTipo = !this.filtroTipo || r.tipo === this.filtroTipo;
      const cumpleEstado = !this.filtroEstado || 
                          (this.filtroEstado === 'visto' && r.visto) ||
                          (this.filtroEstado === 'no-visto' && !r.visto);
      return cumpleTipo && cumpleEstado;
    });
  }

  abrirRecurso(recurso: Recurso) {
    alert(`Abriendo: ${recurso.titulo}`);
  }

  marcarVisto(recurso: Recurso) {
    recurso.visto = !recurso.visto;
  }
}

export default RecursosComponent;
