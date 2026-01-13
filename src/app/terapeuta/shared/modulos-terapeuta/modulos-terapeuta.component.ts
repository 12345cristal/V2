import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ModuloTerapeuta, ModuloEstado } from '../../../interfaces/terapeuta/modulos.interface';

@Component({
  selector: 'app-modulos-terapeuta',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="modulos-section">
      <div class="modulos-header">
        <h2>Módulos Disponibles ({{ modulos.length }})</h2>
        <p class="modulos-subtitle">Acceso a todas las herramientas de terapeuta</p>
      </div>

      <div class="modulos-grid">
        @for (modulo of modulos; track modulo.id) {
          <div [ngClass]="['modulo-card', 'estado-' + modulo.estado]">
            <div class="modulo-icono" [style.backgroundColor]="modulo.color">
              <span class="icon-text">{{ modulo.icono }}</span>
            </div>
            <div class="modulo-info">
              <h3>{{ modulo.nombre }}</h3>
              <p class="modulo-desc">{{ modulo.descripcion }}</p>
              <span class="modulo-estado" [ngClass]="'badge-' + modulo.estado">
                {{ modulo.estado }}
              </span>
            </div>
            <a [routerLink]="modulo.ruta" 
               class="modulo-link"
               [attr.aria-label]="'Ir a ' + modulo.nombre">
              <span class="arrow">→</span>
            </a>

            @if (getEstadoModulo(modulo.id)) {
              <div class="modulo-footer">
                <small>{{ (getEstadoModulo(modulo.id) || {registros_totales: 0}).registros_totales }} registros</small>
                <small [ngClass]="'connected-' + (getEstadoModulo(modulo.id)?.conectado || false)">
                  {{ (getEstadoModulo(modulo.id)?.conectado ? '✓ Conectado' : '✗ Desconectado') }}
                </small>
              </div>
            }
          </div>
        }
      </div>
    </div>
  `,
  styles: [`
    .modulos-section {
      margin-top: 2rem;
      padding: 1.5rem;
      background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
      border-radius: 12px;
      border: 1px solid rgba(0, 0, 0, 0.05);
    }

    .modulos-header {
      margin-bottom: 1.5rem;
    }

    .modulos-header h2 {
      margin: 0;
      font-size: 1.5rem;
      color: #333;
    }

    .modulos-subtitle {
      margin: 0.5rem 0 0;
      color: #666;
      font-size: 0.9rem;
    }

    .modulos-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }

    .modulo-card {
      display: flex;
      flex-direction: column;
      background: white;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
      transition: all 0.3s ease;
      position: relative;
      border: 2px solid transparent;
    }

    .modulo-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    }

    .modulo-card.estado-activo {
      border-color: #4caf50;
    }

    .modulo-card.estado-inactivo {
      opacity: 0.7;
      border-color: #9e9e9e;
    }

    .modulo-card.estado-en-desarrollo {
      border-color: #ff9800;
    }

    .modulo-icono {
      width: 100%;
      height: 80px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2.5rem;
      color: white;
      font-weight: bold;
    }

    .modulo-info {
      flex: 1;
      padding: 1rem;
      display: flex;
      flex-direction: column;
    }

    .modulo-info h3 {
      margin: 0 0 0.5rem;
      font-size: 1.1rem;
      color: #333;
    }

    .modulo-desc {
      margin: 0 0 0.75rem;
      color: #666;
      font-size: 0.85rem;
      line-height: 1.4;
      flex: 1;
    }

    .modulo-estado {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      width: fit-content;
    }

    .badge-activo {
      background-color: #c8e6c9;
      color: #2e7d32;
    }

    .badge-inactivo {
      background-color: #eeeeee;
      color: #616161;
    }

    .badge-en-desarrollo {
      background-color: #ffe0b2;
      color: #e65100;
    }

    .modulo-link {
      position: absolute;
      top: 0;
      right: 0;
      width: 50px;
      height: 80px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(0, 0, 0, 0.05);
      color: #333;
      text-decoration: none;
      transition: all 0.3s ease;
      cursor: pointer;
    }

    .modulo-card:hover .modulo-link {
      background: rgba(0, 0, 0, 0.1);
      color: #000;
    }

    .arrow {
      font-size: 1.5rem;
      font-weight: bold;
    }

    .modulo-footer {
      padding: 0.75rem 1rem;
      background: #fafafa;
      border-top: 1px solid #eee;
      display: flex;
      justify-content: space-between;
      font-size: 0.75rem;
      color: #999;
    }

    .connected-true {
      color: #4caf50;
      font-weight: 600;
    }

    .connected-false {
      color: #f44336;
      font-weight: 600;
    }

    @media (max-width: 768px) {
      .modulos-grid {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class ModulosTerapeutaComponent implements OnInit {
  @Input() modulos: ModuloTerapeuta[] = [];
  @Input() estados: ModuloEstado[] = [];

  ngOnInit() {
    this.inicializarModulos();
  }

  private inicializarModulos() {
    // Si no hay módulos, inicializar con los 15 módulos por defecto
    if (!this.modulos || this.modulos.length === 0) {
      this.modulos = this.getModulosPorDefecto();
    }
  }

  getEstadoModulo(moduloId: string): ModuloEstado | undefined {
    return this.estados.find(e => e.modulo_id === moduloId);
  }

  private getModulosPorDefecto(): ModuloTerapeuta[] {
    return [
      {
        id: 'actividades',
        nombre: 'Actividades',
        descripcion: 'Gestiona tareas y actividades de los niños',
        ruta: '/terapeuta/actividades',
        icono: '✓',
        color: '#4caf50',
        estado: 'activo',
        orden: 1,
      },
      {
        id: 'actividades-list',
        nombre: 'Actividades - Lista',
        descripcion: 'Vista detallada de todas las actividades',
        ruta: '/terapeuta/actividades',
        icono: '📋',
        color: '#66bb6a',
        estado: 'activo',
        orden: 2,
      },
      {
        id: 'asistencias',
        nombre: 'Asistencias',
        descripcion: 'Registro de asistencias y sesiones',
        ruta: '/terapeuta/asistencias',
        icono: '📊',
        color: '#2196f3',
        estado: 'activo',
        orden: 3,
      },
      {
        id: 'horarios',
        nombre: 'Horarios',
        descripcion: 'Gestión de horarios y calendarios',
        ruta: '/terapeuta/horarios',
        icono: '📅',
        color: '#ff9800',
        estado: 'activo',
        orden: 4,
      },
      {
        id: 'inicio',
        nombre: 'Inicio',
        descripcion: 'Dashboard principal y resumen',
        ruta: '/terapeuta/inicio',
        icono: '🏠',
        color: '#9c27b0',
        estado: 'activo',
        orden: 5,
      },
      {
        id: 'mensajes',
        nombre: 'Mensajes',
        descripcion: 'Comunicación y mensajería',
        ruta: '/terapeuta/mensajes',
        icono: '💬',
        color: '#e91e63',
        estado: 'activo',
        orden: 6,
      },
      {
        id: 'ninos',
        nombre: 'Niños',
        descripcion: 'Gestión de perfiles de niños',
        ruta: '/terapeuta/ninos',
        icono: '👶',
        color: '#00bcd4',
        estado: 'activo',
        orden: 7,
      },
      {
        id: 'nino-detalle',
        nombre: 'Detalle del Niño',
        descripcion: 'Información detallada de cada niño',
        ruta: '/terapeuta/ninos/detalle',
        icono: '👤',
        color: '#00acc1',
        estado: 'activo',
        orden: 8,
      },
      {
        id: 'pacientes',
        nombre: 'Pacientes',
        descripcion: 'Gestión de pacientes y registros',
        ruta: '/terapeuta/pacientes',
        icono: '🏥',
        color: '#f44336',
        estado: 'activo',
        orden: 9,
      },
      {
        id: 'paciente-detalle',
        nombre: 'Detalle del Paciente',
        descripcion: 'Información completa de paciente',
        ruta: '/terapeuta/pacientes/detalle',
        icono: '📄',
        color: '#e53935',
        estado: 'activo',
        orden: 10,
      },
      {
        id: 'recomendaciones',
        nombre: 'Recomendaciones',
        descripcion: 'Recomendaciones personalizadas',
        ruta: '/terapeuta/recomendaciones',
        icono: '⭐',
        color: '#ffc107',
        estado: 'activo',
        orden: 11,
      },
      {
        id: 'recomendacion-panel',
        nombre: 'Panel de Recomendaciones',
        descripcion: 'Visualización de recomendaciones',
        ruta: '/terapeuta/recomendaciones',
        icono: '💡',
        color: '#ffb300',
        estado: 'activo',
        orden: 12,
      },
      {
        id: 'recursos',
        nombre: 'Recursos',
        descripcion: 'Biblioteca de recursos terapéuticos',
        ruta: '/terapeuta/recursos',
        icono: '📚',
        color: '#673ab7',
        estado: 'activo',
        orden: 13,
      },
      {
        id: 'recursos-upload',
        nombre: 'Cargar Recursos',
        descripcion: 'Subir nuevos recursos y materiales',
        ruta: '/terapeuta/recursos',
        icono: '⬆️',
        color: '#5e35b1',
        estado: 'activo',
        orden: 14,
      },
      {
        id: 'reportes',
        nombre: 'Reportes',
        descripcion: 'Generación de reportes y análisis',
        ruta: '/terapeuta/reportes',
        icono: '📈',
        color: '#009688',
        estado: 'activo',
        orden: 15,
      },
      {
        id: 'sesiones',
        nombre: 'Sesiones',
        descripcion: 'Registro y seguimiento de sesiones',
        ruta: '/terapeuta/asistencias',
        icono: '🎯',
        color: '#00897b',
        estado: 'activo',
        orden: 16,
      },
    ];
  }
}
