import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Notificacion {
  id: string;
  titulo: string;
  descripcion: string;
  tipo: 'sesion' | 'documento' | 'pago' | 'comentario' | 'reprogramacion';
  fecha: Date;
  leida: boolean;
  enlace?: string;
}

@Component({
  selector: 'app-notificaciones',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="notificaciones-container">
      <h1>🔔 Notificaciones</h1>

      <div class="filtros">
        <button 
          (click)="filtro = 'todas'"
          [class.activo]="filtro === 'todas'"
          class="btn-filtro">
          Todas
        </button>
        <button 
          (click)="filtro = 'no-leidas'"
          [class.activo]="filtro === 'no-leidas'"
          class="btn-filtro">
          No leídas
        </button>
        <button 
          (click)="marcarTodasLeidas()"
          class="btn-limpiar">
          Marcar todas como leídas
        </button>
      </div>

      <div class="notificaciones-list">
        <div *ngFor="let notif of notificacionesFiltradas"
             class="notificacion-card"
             [class.no-leida]="!notif.leida">
          <div class="notif-icon">
            <span *ngIf="notif.tipo === 'sesion'">📅</span>
            <span *ngIf="notif.tipo === 'documento'">📄</span>
            <span *ngIf="notif.tipo === 'pago'">💳</span>
            <span *ngIf="notif.tipo === 'comentario'">💬</span>
            <span *ngIf="notif.tipo === 'reprogramacion'">⏰</span>
          </div>

          <div class="notif-content">
            <h3>{{ notif.titulo }}</h3>
            <p>{{ notif.descripcion }}</p>
            <small>{{ notif.fecha | date: 'short' }}</small>
          </div>

          <div class="notif-estado">
            <button *ngIf="!notif.leida"
                    (click)="marcarComoLeida(notif)"
                    class="btn-leer">
              Marcar leído
            </button>
            <span *ngIf="!notif.leida" class="indicador-nuevo">🆕</span>
          </div>
        </div>

        <div *ngIf="notificacionesFiltradas.length === 0" class="sin-notificaciones">
          <p>{{ filtro === 'no-leidas' ? 'No hay notificaciones sin leer' : 'No hay notificaciones' }}</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .notificaciones-container {
      padding: 2rem;
      max-width: 800px;
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

    .btn-filtro, .btn-limpiar {
      padding: 0.75rem 1.5rem;
      border: 2px solid #ecf0f1;
      background: white;
      color: #2c3e50;
      border-radius: 25px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.3s;

      &:hover {
        border-color: #3498db;
      }

      &.activo {
        background: #3498db;
        color: white;
        border-color: #3498db;
      }
    }

    .btn-limpiar {
      border-color: #95a5a6;
      color: #95a5a6;

      &:hover {
        border-color: #7f8c8d;
        color: #7f8c8d;
      }
    }

    .notificaciones-list {
      display: grid;
      gap: 1rem;
    }

    .notificacion-card {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      display: flex;
      gap: 1rem;
      align-items: flex-start;
      transition: all 0.3s;
      border-left: 4px solid #ecf0f1;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
      }

      &.no-leida {
        background: #f0f8ff;
        border-left-color: #3498db;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
      }
    }

    .notif-icon {
      font-size: 2rem;
      min-width: 50px;
      text-align: center;
    }

    .notif-content {
      flex: 1;

      h3 {
        margin: 0 0 0.5rem 0;
        color: #2c3e50;
      }

      p {
        margin: 0 0 0.5rem 0;
        color: #555;
        line-height: 1.5;
      }

      small {
        color: #7f8c8d;
      }
    }

    .notif-estado {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-shrink: 0;
    }

    .btn-leer {
      padding: 0.5rem 1rem;
      background: #3498db;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.3s;
      white-space: nowrap;

      &:hover {
        background: #2980b9;
        transform: translateY(-2px);
      }
    }

    .indicador-nuevo {
      font-size: 1.2rem;
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% {
        opacity: 1;
      }
      50% {
        opacity: 0.5;
      }
    }

    .sin-notificaciones {
      text-align: center;
      padding: 3rem 1rem;
      color: #95a5a6;

      p {
        margin: 0;
      }
    }

    @media (max-width: 768px) {
      .notificacion-card {
        flex-direction: column;
      }

      .notif-estado {
        width: 100%;
      }

      .btn-leer {
        width: 100%;
      }
    }
  `]
})
export class NotificacionesComponent implements OnInit {
  notificaciones: Notificacion[] = [];
  filtro: 'todas' | 'no-leidas' = 'todas';

  ngOnInit() {
    this.cargarNotificaciones();
  }

  private cargarNotificaciones() {
    this.notificaciones = [
      {
        id: '1',
        titulo: 'Nueva sesión programada',
        descripcion: 'Tu sesión de logopedia ha sido programada para mañana a las 10:00 AM',
        tipo: 'sesion',
        fecha: new Date(),
        leida: false,
      },
      {
        id: '2',
        titulo: 'Nuevo documento disponible',
        descripcion: 'Se ha compartido un nuevo reporte terapéutico',
        tipo: 'documento',
        fecha: new Date(Date.now() - 86400000),
        leida: false,
      },
      {
        id: '3',
        titulo: 'Recordatorio de pago',
        descripcion: 'Tu próximo pago vence el 15 de febrero',
        tipo: 'pago',
        fecha: new Date(Date.now() - 172800000),
        leida: true,
      },
      {
        id: '4',
        titulo: 'Nuevo comentario del terapeuta',
        descripcion: 'La Dra. María García ha dejado un comentario en la última sesión',
        tipo: 'comentario',
        fecha: new Date(Date.now() - 259200000),
        leida: true,
      },
      {
        id: '5',
        titulo: 'Sesión reprogramada',
        descripcion: 'Tu sesión del viernes ha sido movida a jueves a la misma hora',
        tipo: 'reprogramacion',
        fecha: new Date(Date.now() - 345600000),
        leida: true,
      },
    ];
  }

  get notificacionesFiltradas() {
    return this.filtro === 'no-leidas'
      ? this.notificaciones.filter(n => !n.leida)
      : this.notificaciones;
  }

  marcarComoLeida(notif: Notificacion) {
    notif.leida = true;
  }

  marcarTodasLeidas() {
    this.notificaciones.forEach(n => (n.leida = true));
  }
}

export default NotificacionesComponent;

