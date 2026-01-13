// src/app/terapeuta/recomendaciones/recomendaciones.ts
import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RecomendacionService } from '../../service/recomendacion.service';
import { 
  RecomendacionActividad,
  HistorialRecomendacion
} from '../../interfaces/recomendacion.interface';

/**
 * Componente para que los terapeutas vean recomendaciones de actividades
 * para sus pacientes asignados
 */
@Component({
  selector: 'app-terapeuta-recomendaciones',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './recomendaciones.html',
  styleUrls: ['./recomendaciones.scss']
})
export class TerapeutaRecomendacionesComponent implements OnInit {
  // Signals para estado reactivo
  pacientes = signal<any[]>([]);
  pacienteSeleccionado = signal<number | null>(null);
  recomendaciones = signal<RecomendacionActividad[]>([]);
  historial = signal<HistorialRecomendacion[]>([]);
  cargando = signal<boolean>(false);
  mensajeError = signal<string>('');
  mensajeInfo = signal<string>('');
  
  // Configuración
  topN = 5;
  verHistorial = false;

  constructor(
    private recomendacionService: RecomendacionService
  ) {}

  ngOnInit(): void {
    this.cargarPacientesAsignados();
  }

  /**
   * Carga los pacientes asignados al terapeuta actual
   */
  cargarPacientesAsignados(): void {
    this.cargando.set(true);
    this.mensajeError.set('');

    // TODO: Implementar servicio para obtener pacientes del terapeuta
    // Por ahora usamos datos simulados
    setTimeout(() => {
      this.pacientes.set([
        { id: 1, nombre: 'Juan Pérez', edad: 6 },
        { id: 2, nombre: 'María García', edad: 8 },
        { id: 3, nombre: 'Pedro López', edad: 5 }
      ]);
      this.cargando.set(false);
    }, 500);
  }

  /**
   * Obtiene recomendaciones para el paciente seleccionado
   */
  obtenerRecomendaciones(): void {
    const ninoId = this.pacienteSeleccionado();
    if (!ninoId) {
      this.mensajeError.set('⚠️ Por favor selecciona un paciente');
      return;
    }

    this.cargando.set(true);
    this.mensajeError.set('');
    this.recomendaciones.set([]);

    this.recomendacionService.getRecomendacionesInteligentes(ninoId, this.topN, true)
      .subscribe({
        next: (response) => {
          this.recomendaciones.set(response.recomendaciones || []);
          this.mensajeInfo.set(`✓ Se encontraron ${response.recomendaciones?.length || 0} recomendaciones`);
          this.cargando.set(false);
        },
        error: (err) => {
          console.error('Error al obtener recomendaciones:', err);
          this.mensajeError.set(err.error?.detail || 'Error al cargar recomendaciones');
          this.cargando.set(false);
        }
      });
  }

  /**
   * Carga el historial de recomendaciones del paciente
   */
  cargarHistorial(): void {
    const ninoId = this.pacienteSeleccionado();
    if (!ninoId) return;

    this.cargando.set(true);
    this.recomendacionService.getHistorialRecomendaciones(ninoId)
      .subscribe({
        next: (historial) => {
          this.historial.set(historial);
          this.cargando.set(false);
        },
        error: (err) => {
          console.error('Error al cargar historial:', err);
          this.mensajeError.set('Error al cargar historial');
          this.cargando.set(false);
        }
      });
  }

  /**
   * Alternar vista entre recomendaciones y historial
   */
  toggleHistorial(): void {
    this.verHistorial = !this.verHistorial;
    if (this.verHistorial && this.pacienteSeleccionado()) {
      this.cargarHistorial();
    }
  }

  /**
   * Limpiar mensajes después de unos segundos
   */
  limpiarMensajes(): void {
    setTimeout(() => {
      this.mensajeError.set('');
      this.mensajeInfo.set('');
    }, 5000);
  }

  /**
   * Formatear fecha
   */
  formatearFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-MX', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
}



