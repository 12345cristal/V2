import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Tarea {
  id: string;
  titulo: string;
  objetivo: string;
  instrucciones: string;
  fechaAsignacion: Date;
  fechaVencimiento: Date;
  terapeuta: string;
  estado: 'pendiente' | 'realizada' | 'vencida';
  recursos: string[];
}

@Component({
  selector: 'app-tareas',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="tareas-container">
      <h1>📝 Tareas para Casa</h1>
      
      <div class="filtros">
        <button 
          *ngFor="let estado of estados"
          (click)="filtroActual = estado"
          [class.activo]="filtroActual === estado"
          class="filtro-btn">
          {{ estado }}
        </button>
      </div>

      <div class="tareas-lista">
        <div *ngFor="let tarea of tareasFiltradas" 
             class="tarea-card"
             [class]="'estado-' + tarea.estado">
          <div class="tarea-header">
            <h3>{{ tarea.titulo }}</h3>
            <span class="badge" [class]="'badge-' + tarea.estado">
              {{ tarea.estado | uppercase }}
            </span>
          </div>
          
          <p class="objetivo"><strong>Objetivo:</strong> {{ tarea.objetivo }}</p>
          <p class="instrucciones"><strong>Instrucciones:</strong> {{ tarea.instrucciones }}</p>
          <p class="terapeuta"><strong>Asignado por:</strong> {{ tarea.terapeuta }}</p>
          
          <div class="fechas">
            <small>Asignada: {{ tarea.fechaAsignacion | date: 'short' }}</small>
            <small>Vencimiento: {{ tarea.fechaVencimiento | date: 'short' }}</small>
          </div>

          <div class="recursos" *ngIf="tarea.recursos.length > 0">
            <strong>Recursos:</strong>
            <ul>
              <li *ngFor="let recurso of tarea.recursos">{{ recurso }}</li>
            </ul>
          </div>

          <div class="acciones">
            <button (click)="marcarRealizada(tarea)" 
                    *ngIf="tarea.estado === 'pendiente'"
                    class="btn-marcar">
              ✓ Marcar realizada
            </button>
            <button (click)="marcarPendiente(tarea)" 
                    *ngIf="tarea.estado !== 'pendiente'"
                    class="btn-revertir">
              ↶ Revertir
            </button>
          </div>
        </div>

        <div *ngIf="tareasFiltradas.length === 0" class="sin-tareas">
          <p>No hay tareas en esta categoría</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .tareas-container {
      padding: 2rem;
      max-width: 900px;
      margin: 0 auto;
    }

    h1 {
      color: #2c3e50;
      margin-bottom: 2rem;
    }

    .filtros {
      display: flex;
      gap: 1rem;
      margin-bottom: 2rem;
      flex-wrap: wrap;
    }

    .filtro-btn {
      padding: 0.75rem 1.5rem;
      border: 2px solid #ecf0f1;
      background: white;
      border-radius: 25px;
      cursor: pointer;
      transition: all 0.3s;
      font-weight: 600;
      text-transform: capitalize;

      &:hover {
        border-color: #3498db;
      }

      &.activo {
        background: #3498db;
        color: white;
        border-color: #3498db;
      }
    }

    .tareas-lista {
      display: grid;
      gap: 1.5rem;
    }

    .tarea-card {
      background: white;
      border-left: 4px solid #95a5a6;
      border-radius: 8px;
      padding: 1.5rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      transition: all 0.3s;

      &:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
      }

      &.estado-pendiente {
        border-left-color: #e74c3c;
      }

      &.estado-realizada {
        border-left-color: #2ecc71;
        opacity: 0.8;
      }

      &.estado-vencida {
        border-left-color: #f39c12;
      }
    }

    .tarea-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;

      h3 {
        margin: 0;
        color: #2c3e50;
      }
    }

    .badge {
      padding: 0.25rem 0.75rem;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 700;

      &.badge-pendiente {
        background: #ffe5e5;
        color: #c0392b;
      }

      &.badge-realizada {
        background: #e5ffe5;
        color: #27ae60;
      }

      &.badge-vencida {
        background: #fff5e5;
        color: #d68910;
      }
    }

    p {
      margin: 0.5rem 0;
      color: #555;

      strong {
        color: #2c3e50;
      }
    }

    .fechas {
      display: flex;
      gap: 2rem;
      margin: 1rem 0;
      padding: 1rem 0;
      border-top: 1px solid #ecf0f1;
      border-bottom: 1px solid #ecf0f1;

      small {
        color: #7f8c8d;
      }
    }

    .recursos {
      margin: 1rem 0;

      ul {
        list-style: none;
        padding-left: 1.5rem;
        margin: 0.5rem 0 0 0;
      }

      li {
        color: #3498db;
        margin: 0.25rem 0;
        
        &:before {
          content: "📎 ";
          margin-right: 0.5rem;
        }
      }
    }

    .acciones {
      display: flex;
      gap: 1rem;
      margin-top: 1rem;
    }

    .btn-marcar, .btn-revertir {
      padding: 0.5rem 1rem;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.3s;

      &:hover {
        transform: translateY(-2px);
      }
    }

    .btn-marcar {
      background: #2ecc71;
      color: white;

      &:hover {
        background: #27ae60;
      }
    }

    .btn-revertir {
      background: #95a5a6;
      color: white;

      &:hover {
        background: #7f8c8d;
      }
    }

    .sin-tareas {
      text-align: center;
      padding: 2rem;
      color: #95a5a6;

      p {
        margin: 0;
      }
    }
  `]
})
export class TareasComponent implements OnInit {
  tareas: Tarea[] = [];
  filtroActual: string = 'pendiente';
  estados = ['pendiente', 'realizada', 'vencida'];

  ngOnInit() {
    this.cargarTareas();
  }

  private cargarTareas() {
    this.tareas = [
      {
        id: '1',
        titulo: 'Ejercicios de respiración',
        objetivo: 'Mejorar control emocional',
        instrucciones: 'Realizar 5 respiraciones profundas cada 2 horas',
        fechaAsignacion: new Date('2026-01-05'),
        fechaVencimiento: new Date('2026-01-20'),
        terapeuta: 'Dra. María García',
        estado: 'pendiente',
        recursos: ['Video de respiración', 'Guía PDF'],
      },
      {
        id: '2',
        titulo: 'Lectura diaria',
        objetivo: 'Mejorar comprensión lectora',
        instrucciones: 'Leer un cuento de 10 minutos antes de dormir',
        fechaAsignacion: new Date('2026-01-10'),
        fechaVencimiento: new Date('2026-01-25'),
        terapeuta: 'Dra. Carolina López',
        estado: 'realizada',
        recursos: ['Lista de cuentos recomendados'],
      },
    ];
  }

  get tareasFiltradas() {
    return this.tareas.filter(t => t.estado === this.filtroActual);
  }

  marcarRealizada(tarea: Tarea) {
    tarea.estado = 'realizada';
  }

  marcarPendiente(tarea: Tarea) {
    tarea.estado = 'pendiente';
  }
}
